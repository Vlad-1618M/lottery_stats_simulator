# #!/usr/bin/env python
# # -*- config: utf-8 -*-

import sys
import time
import psutil
import orjson
from pathlib import Path
from functools import wraps
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from itertools import combinations
from collections import defaultdict
from bloom_filter2 import BloomFilter
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn

sys.path.append(str(Path(__file__).resolve().parents[1]))
from logger import logger_main

console = Console()
process = psutil.Process()
log_it = logger_main.get_logger(__name__)

# ... timing | perf decorator:
def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        minutes, seconds = divmod(elapsed, 60)
        total = "run time"
        stamp = f"{total:<6} {int(minutes)} [dim]m[/dim] {seconds:>6.2f} [dim]s[/dim] {elapsed:>11.2f}"
        return result, stamp
    return wrapper


@time_it
def find_all_json_paths(base_dir=None):
    if base_dir is None:
        base_dir = Path(__file__).resolve().parents[1]
    result = list(Path(base_dir).glob("*/catalog/*.json"))
    return result


@time_it
def load_json_files_concurrent(paths, batch_size=10, artificial_delay=0, show_logs=True):
    def load_single_file(path_obj, delay=0):
        try:
            if delay:
                time.sleep(delay)
            with path_obj.open("rb") as loaded_file:
                return path_obj.name, orjson.loads(loaded_file.read())
        except Exception:
            return path_obj.name, None

    data = {}
    total_files = len(paths)
    total_batches = (total_files + batch_size - 1) // batch_size

    for batch_index in range(total_batches):
        start_idx = batch_index * batch_size
        end_idx = min(start_idx + batch_size, total_files)
        batch_paths = paths[start_idx:end_idx]

        if show_logs:
            console.print(f"[bold][Batch {batch_index + 1}/{total_batches}][/bold] [bold_yellow]Processing:[/bold_yellow] {len(batch_paths)} files ...\n")

        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_file = {executor.submit(load_single_file, path, artificial_delay): path.name for path in batch_paths}

            for future in as_completed(future_to_file):
                name, content = future.result()
                if content:
                    data[name] = content
                if show_logs:
                    console.print(f"\t→ [dim]Loading:[/dim] {name}")

        if show_logs:
            console.print(f"\t[green]✓ Batch {batch_index + 1} completed! {end_idx}/{total_files} files done:\n[/green]")

    return data


@time_it
def extract_sequences(data, min_sequence_length=None):
    if min_sequence_length < 1:
        raise ValueError("min_sequence_length must be >= 1")
    sequences = defaultdict(list)
    for filename, records in data.items():
        for record in records:
            selection = record.get("selection", {})
            game = record.get("game", "unknown")
            for key, numbers in selection.items():
                if isinstance(numbers, list) and len(numbers) >= min_sequence_length:
                    num_tuple = tuple(sorted(numbers))
                    bloom = BloomFilter(max_elements=100, error_rate=0.01)
                    for num in num_tuple:
                        bloom.add(num)
                    sequences[filename].append((game, key, num_tuple, bloom))
    return sequences


@time_it
def compare_sequences(sequences, depth=1, min_overlap_count="auto", min_overlap_percent=0, strict_key_match=False, same_game_only=False, game_filter=None, exclude_keys=None,):
    exact_matches = defaultdict(list)
    partial_matches = defaultdict(list)
    file_pairs = list(combinations(sequences.items(), 2))

    exact_count = 0
    partial_count = 0
    sequence_comparisons = 0
    total_sequence_in_file_one = 0
    total_sequence_in_file_two = 0

    exclude_keys = exclude_keys or set()

    log_it.info("Starting sequence comparison:")
    log_it.info(f"Total JSON files: {len(sequences)}")
    log_it.info(f"Total file pairs to compare: {len(file_pairs)}\n")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(),
                  TextColumn("[bright_white]Pairs[/bright_white]: {task.completed}/{task.total} [bright_green]Exact:[/bright_green] {task.fields[exact]} [dim]Partial[/dim]: {task.fields[partial]}"),
                  TimeElapsedColumn(), TimeRemainingColumn(), TextColumn("[bold blue]Runtime:[/bold blue]{task.percentage:>3.0f}%"), ) as progress:

        task = progress.add_task("[magenta]Comparing sequences...", total=len(file_pairs), exact=0, partial=0)

        for (json_one, sequences_one), (json_two, sequences_two) in file_pairs:
            total_sequence_in_file_one += len(sequences_one)
            total_sequence_in_file_two += len(sequences_two)

            for game_one, key_game_one, seq1, bloom1 in sequences_one:
                for game_two, key_game_two, seq2, bloom2 in sequences_two:
                    sequence_comparisons += 1

                    # _____ Skip conditions _____
                    if key_game_one in exclude_keys or key_game_two in exclude_keys:
                        continue
                    if strict_key_match and key_game_one != key_game_two:
                        continue
                    if same_game_only and game_one != game_two:
                        continue
                    if game_filter and (game_one != game_filter or game_two != game_filter):
                        continue
                    if not any(n in bloom2 for n in seq1):
                        continue

                    current_min = (max(depth, min(len(seq1), len(seq2)) // 2) if min_overlap_count == "auto" else min_overlap_count)

                    # --- Exact match ---
                    if seq1 == seq2:
                        exact_matches[(json_one, json_two)].append((game_one, key_game_one, game_two, key_game_two, list(seq1), len(seq1), len(seq2)))
                        exact_count += 1

                    else:
                        overlap = set(seq1).intersection(seq2)
                        overlap_count = len(overlap)
                        max_size = max(len(seq1), len(seq2), 1)
                        overlap_percent = (overlap_count / max_size) * 100

                        if (overlap_count >= depth and overlap_count >= current_min and overlap_percent >= min_overlap_percent):
                            partial_matches[(json_one, json_two)].append((game_one, key_game_one, game_two, key_game_two, sorted(overlap), len(seq1), len(seq2)))
                            partial_count += 1

            progress.update(task, advance=1, exact=exact_count, partial=partial_count)

    # --- Log Stats Queue ---
    log_it.info(f" → Total sequences in file1: {total_sequence_in_file_one}")
    log_it.info(f" → Total sequences in file2: {total_sequence_in_file_two}")
    log_it.info(f" → Avg sequences per file: {(total_sequence_in_file_one + total_sequence_in_file_two) // max(len(file_pairs) * 2, 1)}")
    log_it.info(f" → Total sequence comparisons: {sequence_comparisons}")
    log_it.info(f" ✓ Exact matches found: {exact_count}")
    log_it.info(f" ✓ Partial matches found: {partial_count}")

    comparison_stats = {
        "File Pairs Compared": len(file_pairs),
        "Sequences Total for .json # 1": total_sequence_in_file_one,
        "Sequences Total for .json # 2": total_sequence_in_file_two,
        "Average Sequences/File": (total_sequence_in_file_one + total_sequence_in_file_two) // max(len(file_pairs) * 2, 1),
        "Sequence Comparisons": sequence_comparisons,
        "Exact Matches": exact_count,
        "Partial Matches": partial_count}

    return exact_matches, partial_matches, comparison_stats


# ____________________________________________________________________________________________________________________________________________________________
@time_it
def display_matches(title, matches, view=(True, True), console=None, max_display_rows=10):
    console = console or Console()
    if not matches:
        return

    show_panel, show_table = view  # <- tuple unpacking | view params:
    if show_panel:
        panel = Panel(f"[bold green]{title}[/bold green]", width=80, subtitle=f"[dim]{len(matches)} file pairs[/dim]")
        console.print(panel)
    if show_table:
        shown_rows = 0
        for (file1, file2), match_list in matches.items():
            if shown_rows >= max_display_rows:
                break  # don't show more than allowed

            table = Table(title=f"{file1} ↔ {file2}", show_lines=False, width=80, title_justify="left")
            table.add_column("File 1 Game/Key", style="cyan")
            table.add_column("File 2 Game/Key", style="magenta")
            table.add_column("Matching Values", style="green")
            table.add_column("Match Depth", justify="right")

            for (game_one, key_one, game_two, key_two, values, first_sequence_length, second_sequence_length) in match_list:
                if shown_rows >= max_display_rows:
                    break

                max_size = max(first_sequence_length, second_sequence_length, 1)
                depth_percent = int((len(values) / max_size) * 100)

                if depth_percent == 100:
                    color = "bold green"
                elif depth_percent >= 75:
                    color = "green"
                elif depth_percent >= 50:
                    color = "yellow"
                elif depth_percent >= 25:
                    color = "orange1"
                else:
                    color = "red"

                depth_display = f"[{color}]{depth_percent}%[/{color}]"
                table.add_row(f"{game_one} [{key_one}]", f"{game_two} [{key_two}]", str(values), depth_display)
                shown_rows += 1

            console.print(table)

        remaining = sum(len(v) for v in matches.values()) - shown_rows
        if remaining > 0:
            console.print(f"[dim]+ {remaining} more matches not shown (use --max_partial or --max_exact to adjust)[/dim]\n")


# ____________________________________________________________________________________________________________________________________________________________
    # if show_table:
    #     for (file1, file2), match_list in matches.items():
    #         table = Table(title=f"{file1} ↔ {file2}", show_lines=False, width=80, title_justify="left")
    #         table.add_column("File 1 Game/Key", style="cyan")
    #         table.add_column("File 2 Game/Key", style="magenta")
    #         table.add_column("Matching Values", style="green")
    #         table.add_column("Match Depth", justify="right")
    #         for (game_one, key_one, game_two, key_two, values, first_sequence_length, second_sequence_length) in match_list:
    #             max_size = max(first_sequence_length, second_sequence_length, 1)
    #             depth_percent = int((len(values) / max_size) * 100)
    #             if depth_percent == 100:
    #                 color = "bold green"
    #             elif depth_percent >= 75:
    #                 color = "green"
    #             elif depth_percent >= 50:
    #                 color = "yellow"
    #             elif depth_percent >= 25:
    #                 color = "orange1"
    #             else:
    #                 color = "red"

    #             depth_display = f"[{color}]{depth_percent}%[/{color}]"
    #             table.add_row(f"{game_one} [{key_one}]", f"{game_two} [{key_two}]", str(values), depth_display)
    #         console.print(table)

# ____________________________________________________________________________________________________________________________________________________________


@time_it
def display_summary(exact, partial, console=None, max_exact_rows=50, max_partial_rows=10):
    console = console or Console()
    total_exact = sum(len(value) for value in exact.values())
    total_partial = sum(len(value) for value in partial.values())
    table = Table(title="\nSequence Match Summary:", width=170, show_header=True, header_style="bold cyan", show_lines=True, title_justify="left")

    # ____ built columns:
    table.add_column("Match Type", justify="left", style="cyan")
    table.add_column("Count", justify="right", style="yellow")
    table.add_column("Details", style="green")

    # ____ format match details | helper function:
    def format_match_details(matches, is_exact=False):
        details = []
        for (file_one_info, file_two_info), match_list in matches.items():
            
            for game_one, game_one_key_one, game_two, game_two_key_two, values, sequence_length_one, sequence_length_two in match_list:
                match_percent = 100 if is_exact else int((len(values) / max(sequence_length_one, sequence_length_two)) * 100)
                color = "green" if is_exact else ("bold green" if match_percent >= 75 else "bold yellow" if match_percent >= 50 else "bold orange1" if match_percent >= 25 else "red")

                detail_str = (
                    f"[bright_white]{file_one_info.capitalize()}[/bright_white] [bold]↔[/bold] [bright_white]{file_two_info.capitalize()}[/bright_white]\n"
                    f"[bright_blue]{game_one.upper()}[/bright_blue]: in [bright_blue].json[/bright_blue] key name: [dim]{game_one_key_one}[/dim] [bold]→[/bold] "
                    f"[cyan]{game_two.upper()}[/cyan]: in [cyan].json[/cyan] key name: [dim]{game_two_key_two}[/dim]\n"
                    f"\t\t• [bold]Match[/bold]: [{color}]{match_percent}%[/{color}] • Values: [bright_green]{values}[/bright_green]\n")
                details.append(detail_str)
        return details

    # __ configure exact matches:
    if exact:
        exact_details = format_match_details(exact, is_exact=True)
        table.add_row("[bold green]Exact Matches[/bold green]", f"[bold green]{total_exact}[/bold green]", "\n".join(exact_details[:max_exact_rows]))
        if total_exact > max_exact_rows:
            table.add_row("", "", f"[bold]+[/bold] [bright_green]{total_exact - max_exact_rows}[/bright_green] [dim]more exact matches...[/dim]")

    # __ configure partial matches:
    if partial:
        partial_details = format_match_details(partial)
        table.add_row("[bold yellow]Partial Matches[/bold yellow]", str(total_partial), "\n".join(partial_details[:max_partial_rows]))
        if total_partial > max_partial_rows:
            table.add_row("", "", f"[bold]+[/bold] [bright_yellow]{total_partial - max_partial_rows}[/bright_yellow] [dim]more partial matches:[/dim] run [bold]→[/bold] display_matches(view=(True, True) to see details:")
    console.print(table)


def main(main_depth_level: int, minimum_sequence: int, games=None, logs=None, console=None, max_exact=10, max_partial=3, save_all_to_html=False,):
    console = console or Console()
    overall_start = time.perf_counter()
    timings = {}

    paths, timings['Find JSON'] = find_all_json_paths()
    if not paths:
        console.print(f"\n[yellow]No JSON files found[/yellow]: [dim]{paths}[/dim]\n[dim]Try:[/dim] → [bold green]quickPick.py[/bold green]")
        return

    data, timings['Load JSON'] = load_json_files_concurrent(paths, batch_size=10, artificial_delay=0, show_logs=logs)
    sequences, timings['Extract Sequences'] = extract_sequences(data, min_sequence_length=minimum_sequence)
    (exact, partial, math_stats), timings['Compare Sequences'] = compare_sequences(sequences,
                                                                                   depth=main_depth_level,
                                                                                   min_overlap_percent=30,
                                                                                   min_overlap_count="auto",
                                                                                   exclude_keys=None,
                                                                                   strict_key_match=True,
                                                                                   same_game_only=False,
                                                                                   game_filter=games)

    _, timings['Display Exact Matches'] = display_matches("Exact Matches", exact, view=(False, False), console=console)
    _, timings['Display Partial Matches'] = display_matches("Partial Matches", partial, view=(False, False), console=console)
    _, timings['Display Summary'] = display_summary(exact, partial, console=console, max_exact_rows=max_exact, max_partial_rows=max_partial,)

    overall_time = time.perf_counter() - overall_start
    minutes, seconds = divmod(overall_time, 60)
    mem_mb = process.memory_info().rss / (1024 * 1024)

    bench_table = Table(title="\n[bright_magenta]Benchmark Summary[/bright_magenta]:", show_lines=False, title_justify="center", box=None)
    bench_table.add_column("JOB/TASK:\n", justify="left", style="bright_cyan", no_wrap=False)
    bench_table.add_column("Duration:\n", style="yellow", justify="right")

    for task, duration in timings.items():
        bench_table.add_row(task, f"{duration}: [bold green]s[/bold green]")

    bench_table.add_row("[magenta]─[/magenta]" * 25, "")

    if math_stats:
        for key, val in math_stats.items():
            bench_table.add_row(key, f"{val:,}")

        bench_table.add_row("[bright_magenta]─[/bright_magenta]" * 25, "")
        bench_table.add_row("Total Time", f"{minutes:.0f} min {seconds:.2f} sec")
        bench_table.add_row("Max Memory", f"{mem_mb:.2f} MB")

    if save_all_to_html and console.record:
        display_matches("Exact Matches", exact, view=(True, True), console=console, max_display_rows=max_exact)
        display_matches("Partial Matches", partial, view=(True, True), console=console, max_display_rows=max_partial)
        # display_matches("Partial Matches", partial, view=(True, True), console=console)

    bench_table.add_row("[dim]-[/dim]" * 25, "")
    bench_table.add_row("[bold green]Total Time[/bold green]:", f"[bold green]{minutes}[/bold green] [dim]minutes[/dim]: [bold magenta]{seconds:.2f}[/bold magenta] [dim]seconds[/dim]:")
    bench_table.add_row("[bold magenta]Max Memory[/bold magenta]:", f"[bold magenta]{mem_mb:.2f} MB[/bold magenta]")

    console.print(bench_table)
    console.print("[dim]=[/dim]" * 70, "\n")


if __name__ == "__main__":
    # pass
    filter_test = ["megamillion", "powerball", "lotto", "luckyday", "pick3", "pick4"]
    main(main_depth_level=1, minimum_sequence=5, games=filter_test[0], logs=False)
