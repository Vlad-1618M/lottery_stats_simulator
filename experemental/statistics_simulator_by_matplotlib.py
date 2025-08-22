#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import argparse
import warnings
import threading
import orjson as json
from pathlib import Path
from collections import deque
import matplotlib.pyplot as plt
from itertools import combinations, islice
from bloom_filter2 import BloomFilter
import matplotlib.animation as animation
from queue import Queue
import random
import signal
import sys

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# ___________________________________ Game Sequences Requirements ___________________________________
AVAILABLE_GAMES = ["megamillion", "powerball", "lotto", "luckyday", "pick3", "pick4"]
MIN_SEQ_MAP = {"lotto": 6, "megamillion": 5, "powerball": 5, "luckyday": 5, "pick3": 3, "pick4": 4}

# ___________________________________ Args Parser ___________________________________
parser = argparse.ArgumentParser(
    description="""
Live Lotto Stats Visualizer with optional simulation and chart export.

Examples:
  python3 script.py --simulate --all --export-after 30
  python3 script.py --games megamillion powerball --count 500
  python3 script.py --all --min-sequence 5 --max-pairs 300
  python3 script.py --simulate --export-after 45
""",
    formatter_class=argparse.RawTextHelpFormatter
)

group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("--all", action="store_true", help="Run all supported games")
group.add_argument("--games", nargs="+", choices=AVAILABLE_GAMES, help="Run specific games")

parser.add_argument("--min-sequence", type=int, help="Override default sequence length")
parser.add_argument("--max-pairs", type=int, default=300, help="Max sequence comparisons per frame (default: 300)")
parser.add_argument("--simulate", action="store_true", help="Run in fake data mode (or fallback if no JSON found)")
parser.add_argument("--count", type=int, default=1000, help="Number of fake records to simulate (default: 1000)")
parser.add_argument("--export-after", type=int, help="Export chart to PNG after N seconds and exit")

args = parser.parse_args()

# ___________________________________ Global Settings ___________________________________
SRC = Path(__file__).resolve().parents[1]
CATALOG_DIRS = list(SRC.glob("*/catalog"))
JSON_PATHS = sorted([p for d in CATALOG_DIRS for p in d.glob("*.json")])

GAMES = AVAILABLE_GAMES if args.all or not args.games else args.games
MIN_SEQ = args.min_sequence
MAX_PAIRS = args.max_pairs
simulate_mode = args.simulate or not JSON_PATHS
FAKE_COUNT = args.count

# ___________________________________ Stats ___________________________________
STATS = {
    "File Pairs Compared": 0,
    "Sequence Comparisons": 0,
    "Exact Matches": 0,
    "Partial Matches": 0,
    "Bloom Filter Hits": 0,
}

FILE_LOG = deque(maxlen=30)
BLOOM = BloomFilter(max_elements=10000, error_rate=0.001)
SELECTION_QUEUE = Queue()
SELECTION_STORE = deque(maxlen=10000)
LOCK = threading.Lock()

bloom_growth = []
exact_match_growth = []
partial_match_growth = []
ticks = []

def handle_exit(sig, frame):
    print("\n[EXIT] Ctrl+X detected. Shutting down gracefully...")
    plt.close('all')
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)


def extract_numbers(selection: dict) -> set:
    numbers = set()
    for v in selection.values():
        if isinstance(v, list):
            numbers.update(v)
    return numbers

def simulate_fake_selection(game):
    count = MIN_SEQ_MAP.get(game, 5)
    max_num = 70 if game in ("megamillion", "powerball") else 50
    return {
        "primary": sorted(random.sample(range(1, max_num), count)),
        "bonus": sorted(random.sample(range(1, 26), 1)) if game in ("megamillion", "powerball") else []
    }

def process_json_files():
    if simulate_mode:
        fake_files = [f"player_{i}.json" for i in range(FAKE_COUNT)]
        for name in fake_files:
            game = random.choice(GAMES)
            selection = simulate_fake_selection(game)
            numbers = extract_numbers(selection)
            required = MIN_SEQ if MIN_SEQ else MIN_SEQ_MAP.get(game, 5)

            if len(numbers) < required:
                continue

            numbers_tuple = tuple(sorted(numbers))
            with LOCK:
                if numbers_tuple in BLOOM:
                    STATS["Bloom Filter Hits"] += 1
                else:
                    BLOOM.add(numbers_tuple)
                    SELECTION_QUEUE.put(set(numbers))
                FILE_LOG.appendleft(name)

            time.sleep(0.005)
    else:
        for file in JSON_PATHS:
            try:
                data = json.loads(file.read_bytes())
                for entry in data:
                    game = entry.get("game")
                    if game not in GAMES:
                        continue
                    selection = entry.get("selection", {})
                    numbers = extract_numbers(selection)
                    required = MIN_SEQ if MIN_SEQ else MIN_SEQ_MAP.get(game, 5)
                    if len(numbers) < required:
                        continue

                    numbers_tuple = tuple(sorted(numbers))
                    with LOCK:
                        if numbers_tuple in BLOOM:
                            STATS["Bloom Filter Hits"] += 1
                        else:
                            BLOOM.add(numbers_tuple)
                            SELECTION_QUEUE.put(set(numbers))

                with LOCK:
                    try:
                        name = file.name
                        name.encode("ascii")
                    except UnicodeEncodeError:
                        name = f"(unicode: {file.stem})"
                    FILE_LOG.appendleft(name)
            except Exception:
                continue

def compare_sequences():
    while True:
        try:
            new_seq = SELECTION_QUEUE.get(timeout=2)
            SELECTION_STORE.append(new_seq)
            pairs = islice(combinations(SELECTION_STORE, 2), MAX_PAIRS)
            count = exact = partial = 0
            for a, b in pairs:
                shared = a & b
                count += 1
                if len(shared) >= min(len(a), len(b)) and shared:
                    exact += 1
                elif len(shared) >= 2:
                    partial += 1
            with LOCK:
                STATS["Exact Matches"] += exact
                STATS["Partial Matches"] += partial
                STATS["Sequence Comparisons"] += count
                STATS["File Pairs Compared"] = len(SELECTION_STORE)
        except BaseException:
            time.sleep(0.1)


fig, axs = plt.subplots(2, 2, figsize=(18, 10), facecolor="black")
ax_stats = axs[0][0]
ax_files = axs[0][1]
ax_bloom = axs[1][0]
ax_growth = axs[1][1]

def update_plot(frame):
    ax_stats.clear()
    ax_files.clear()
    ax_bloom.clear()
    ax_growth.clear()

    with LOCK:
        labels = list(STATS.keys())
        values = list(STATS.values())
        bars = ax_stats.barh(labels, values, color=["cyan", "blue", "green", "orange", "magenta"])
        for bar, val in zip(bars, values):
            width = bar.get_width()
            ax_stats.text(width + 1, bar.get_y() + bar.get_height() / 2, f"{val}", color="white", va="center", fontsize=10)

        max_val = max(values) if values else 10
        ax_stats.set_xlim(0, max(10, max_val * 1.2))
        ax_stats.set_facecolor("black")
        ax_stats.tick_params(colors="white", labelsize=10)
        ax_stats.set_title("Live Statistics", color="white", fontsize=14)

        ax_files.set_facecolor("black")
        ax_files.set_title("Recent JSON Files Processed", color="white", fontsize=14)
        ax_files.set_xticks([])
        ax_files.set_yticks([])
        for i, name in enumerate(list(FILE_LOG)[::-1]):
            ax_files.text(0.05, 0.95 - i * 0.03, name, color="cyan", fontsize=8, transform=ax_files.transAxes)

        ticks.append(len(ticks) + 1)

        def append_growth(growth_list, stat_key):
            current = STATS[stat_key]
            if not growth_list or current != growth_list[-1]:
                growth_list.append(current)
            else:
                growth_list.append(growth_list[-1])

        append_growth(bloom_growth, "Bloom Filter Hits")
        append_growth(exact_match_growth, "Exact Matches")
        append_growth(partial_match_growth, "Partial Matches")

        ax_bloom.plot(ticks, bloom_growth, color="magenta", marker="o", linestyle="-", label="Bloom Hits")
        ax_bloom.set_title("Bloom Filter Growth", color="white")
        ax_bloom.set_facecolor("black")
        ax_bloom.tick_params(colors="white")
        ax_bloom.set_xlabel("Time (ticks)", color="white")
        ax_bloom.set_ylabel("Hits", color="white")
        ax_bloom.legend(loc="upper left", facecolor="black", edgecolor="white", labelcolor="white")

        ax_growth.plot(ticks, exact_match_growth, color="green", marker=".", linestyle="-", label="Exact")
        ax_growth.plot(ticks, partial_match_growth, color="orange", marker=".", linestyle="-", label="Partial")
        ax_growth.set_title("Match Growth", color="white")
        ax_growth.set_facecolor("black")
        ax_growth.tick_params(colors="white")
        ax_growth.set_xlabel("Time (ticks)", color="white")
        ax_growth.set_ylabel("Matches", color="white")
        ax_growth.legend(loc="upper left", facecolor="black", edgecolor="white", labelcolor="white")

        fig.suptitle(f"Games: {', '.join(GAMES)} | MaxPairs={MAX_PAIRS} | FakeRecords={FAKE_COUNT if simulate_mode else 'N/A'}",
                     color="white", fontsize=16)

def export_and_exit_timer(seconds: int):
    print(f"[INFO] Exporting chart after {seconds} seconds...")
    time.sleep(seconds)
    output_path = Path(f"lotto_chart_{int(time.time())}.png")
    fig.savefig(output_path, facecolor='black', dpi=300)
    print(f"[DONE] Chart saved to: {output_path}")
    plt.close('all')
    sys.exit(0)


loader_thread = threading.Thread(target=process_json_files, daemon=True)
compare_thread = threading.Thread(target=compare_sequences, daemon=True)
loader_thread.start()
compare_thread.start()

ani = animation.FuncAnimation(fig, update_plot, interval=200)

if args.export_after:
    timer_thread = threading.Thread(target=export_and_exit_timer, args=(args.export_after,), daemon=True)
    timer_thread.start()

plt.show()
