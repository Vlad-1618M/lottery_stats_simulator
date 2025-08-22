#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from pathlib import Path
from rich.panel import Panel
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
from math_modules.sieve_eratosthenes_algo_prime_numbers import external_calls
console = Console()

def cli(*cmd, live_output=False, **options):
    defaults = {"capture_output": not live_output, "text": True}
    merged = {**defaults, **options}

    if live_output:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')
        process.wait()
    else:
        run = subprocess.run(cmd, **merged)
        print(run.stdout)


def info_statement(explain_primes=False):
    thought = "🤔"
    # cool = "😎"
    # index_down = "👇"
    # index_right = "👉"
    # thumbs_up = "👍"
    жопа = "🔴"
    victory = "✌️"
    index_up = "☝️"
    game_sample = ["megamillion", "powerball", "lotto", "luckyday", "pick3", "pick4"]

    players_config = Path(__file__).resolve().parents[1] / "injectors"
    games_config = Path(__file__).resolve().parents[1] / "globs"
    players = [_ for _ in players_config.iterdir() if _.is_file() and _.suffix == ".yml"]
    games = [_ for _ in games_config.iterdir() if _.is_file() and _.suffix == ".yml"]

    nlp = f"""
    [italic green]Illinois State [yellow]Lottery Quick-Pick[/yellow] Number Generator[/italic green]:

    [magenta]Food for Thought[/magenta]:
        [italic]Math is everywhere:
        [green]Some[/green] just [green]know[/green] and use [bright_green]strategy[/bright_green] to change the outcome[/italic], [italic dim]others[/italic dim] keep guessing with hope and plain randomness ...
        [italic]So, I thought to myself[/italic], '[italic green] ... why not attach a control nub to my luck[/italic green], [italic magenta]make [italic yellow]QuickPick[/italic yellow] less boring[/italic magenta]'
        ... [italic]that turned out to be a fun excersize:[/italic]

    [magenta]Why do it ? [/magenta] {thought}
        Unlike typical [yellow]QuickPick[/yellow] options in every lotto game across America ...
        This program intensifies [magenta]Prime Number(s)[/magenta] selections to be included in random generation sequence [magenta]e.g[/magenta] [italic yellow]alternative QuickPick[/italic yellow]
        [dim]─────────────────────────────────────────────────────────────────────────────────────────---------------------------------[/dim]

    The [magenta]quickPick.py[/magenta] script [dim]routine[/dim] [magenta]options[/magenta]:

        [cyan]{sys.argv[0]}[/cyan] [magenta]args:[/magenta]
            [yellow]--auto[/yellow]           Run in auto-mode: [red]NO[/red] [dim]sequence confirmations[/dim]
            [yellow]--all-names[/yellow]      Apply selection to all available [bold green]names[/bold green] specified in [bright_magenta]{(Path(*players).name)}[/bright_magenta]
            [yellow]--run-all[/yellow]        Process all available games defined in [bright_magenta]{(Path(*games).name)}[/bright_magenta]
            [yellow]--seed[/yellow] [green]NUMBER[/green]    Set random seed for reproducible results: [red]random is OFF[/red] [dim]static sequence only[/dim]
            [yellow]--game[/yellow] [green]NAME[/green]      Specify which game to run: [yellow][[/yellow][italic dim] {', '.join(game_sample)} [/italic dim][yellow]][/yellow]
            [yellow]-h[/yellow], [green]--help[/green]       Show this help message:

        [magenta]call examples[/magenta]:
            [cyan]{sys.argv[0]}[/cyan] [yellow]--auto[/yellow]
            [cyan]{sys.argv[0]}[/cyan] [yellow]--auto --all-names[/yellow]
            [cyan]{sys.argv[0]}[/cyan] [yellow]--auto --all-names --game[/yellow] [italic dim]megamillion[/italic dim]
            [cyan]{sys.argv[0]}[/cyan] [yellow]--auto --all-names --game[/yellow] [italic dim]powerball[/italic dim]
            [cyan]{sys.argv[0]}[/cyan] [yellow]--auto --all-names --game[/yellow] [italic dim]luckyday[/italic dim]
            [cyan]{sys.argv[0]}[/cyan] [yellow]--auto --all-names --game[/yellow] [italic dim]lotto[/italic dim]
            [cyan]{sys.argv[0]}[/cyan] [yellow]--run-all[/yellow]

            {index_up}\tThe lotto [yellow]--game[/yellow] type argument offers a selector name interaction using pre-recorded names from [bright_magenta]{(Path(*players).name)}[/bright_magenta]:
            [dim]With a[/dim] [magenta]grid-based[/magenta] [dim]output and adjustable[/dim] [magenta]row[/magenta] [dim]display range[/dim] - [dim]Enter[/dim] the [magenta]row[/magenta] count,
            follow [green]y[/green] or [red]n[/red] promt untill [dim]acceptable name[/dim] is [green]shown[/green], [dim]enter[/dim] selceted player name, [green]run[/green] the game:

            [magenta]call examples[/magenta]:
                [cyan]{sys.argv[0]}[/cyan] [yellow]--game[/yellow] [italic dim]megamillion[/italic dim]
                [cyan]{sys.argv[0]}[/cyan] [yellow]--game[/yellow] [italic dim]powerball[/italic dim]
                [cyan]{sys.argv[0]}[/cyan] [yellow]--game[/yellow] [italic dim]lotto[/italic dim]
                [cyan]{sys.argv[0]}[/cyan] [yellow]--game[/yellow] [italic dim]luckyday[/italic dim]
                [cyan]{sys.argv[0]}[/cyan] [yellow]--game[/yellow] [italic dim]megamillion[/italic dim]
                [cyan]{sys.argv[0]}[/cyan] [yellow]--game[/yellow] [italic dim]powerball[/italic dim] [italic red]--seed 42[/italic red]

            [cyan]{sys.argv[0]}[/cyan] [yellow]--sieve[/yellow] [italic dim]Learn how prime numbers work using Sieve of Eratosthenes algo [/italic dim]
            [dim]─────────────────────────────────────────────────────────────────────────────────────────----------------------[/dim]

            {index_up}\t[italic]For those whose first language is [bright_red]not[/bright_red] English the [/italic] [underline dim]'GoogleTranslator'[/underline dim] [italic]API is included [/italic]

                [dim]Step[/dim]: [yellow]1[/yellow] run [cyan]{sys.argv[0]}[/cyan] [dim green]--sieve[/dim green] [yellow]--langs[/yellow] [dim]view availble languages[/dim]
                [dim]Step[/dim]: [green]2[/green] re-run [cyan]{sys.argv[0]}[/cyan] [dim green]--sieve[/dim green] [yellow]--lang[/yellow] [dim]launuage code[/dim]

                [magenta]call examples[/magenta]:
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]sr[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Serbian[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]es[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Spanish[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]ru[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Russian[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]hy[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Armenian[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]fa[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Persian[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]iw[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Hebrew[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]is[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Icelandic[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]zh-TW[/bold] [dim]|[/dim] [dim]->[/dim] [dim cyan]Chinese(traditional)[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]hi[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Hindi[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]ko[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Korean[/dim cyan]
                    [cyan]{sys.argv[0]}[/cyan] [green]--sieve[/green] [yellow]--lang[/yellow] [bold]ja[/bold]    [dim]|[/dim] [dim]->[/dim] [dim cyan]Japanese[/dim cyan]

    [dim]─────────────────────────────────────────────────────────────────────────────────────────----------------------[/dim]
    Probability favors the prepared. [italic dim]or so they say ...
    I wonder, how primes, might shift our odds ...
    and I hope the idea of prime-selections introduces measurable strategy or simply a Dopamine boost:[/italic dim] {victory}

    [italic dim]P.S.[/italic dim] until the day all lottos go from [bright_green]Combination[/bright_green] to [bright_red]Permutation[/bright_red] sequence, then its [bold red]game over[/bold red] {жопа} """

    if explain_primes:
        external_calls(["--algo"])
        # external_calls(["--algo", "--lang", "es"])
        # external_calls(["--lang", "es"])
        # external_calls(["--langs"])

    console.print(Panel(f"[bold]{nlp}[/bold]", title="QuickPick Args: Help"), width=160)
    sys.exit(0)


if __name__ == "__main__":
    info_statement(explain_primes=False)
