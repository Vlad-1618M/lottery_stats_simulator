#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import cProfile
import subprocess
from pathlib import Path
from typing import Callable
# from pstats import SortKey
# import cProfile, pstats, io  # noqa: E401

sys.path.append(str(Path(__file__).resolve().parents[1]))

def perf_stats(function: Callable, stat_file: str = "profile.prof", open_viz: bool = True):
    """Profile a function | run SnakeViz optionally:
        Args:
            function: Callable to profile
            stat_file: Output .prof filename
            open_viz: If True, auto-launches SnakeViz"""
    profiler = cProfile.Profile()
    profiler.enable()
    function()
    profiler.disable()
    profiler.dump_stats(stat_file)

    if open_viz:
        cli("snakeviz", stat_file)

# def cli(*cmd, **options):
#     defaults = {"capture_output": True, "text": True}
#     merged = {**defaults, **options}
#     run = subprocess.run(cmd, **merged)
#     print(run.stdout)

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

def date_gen_load(limit, out=False):
    counter = 0
    while counter < limit:
        print(f"Count: {counter}")
        cli("python3", "src/quickPick.py", "--auto", "--all-names", live_output=out)
        counter += 1


if __name__ == "__main__":
    # date_gen_load(limit=2, out=True)
    date_gen_load(limit=3, out=False)
    # perf_stats(games(player="natata", language_catalog=False, csv_file=False, md_file=False), "gamerecs.prof", open_viz=False)
    # perf_stats(t, "gamerecs.prof", open_viz=False)
    # perf_stats(main(player="", language_catalog=False, csv_file=False, md_file=False), "gamerecs.prof", open_viz=True)
    # perf_stats(lambda: your_function(arg1, arg2), "output.prof")
