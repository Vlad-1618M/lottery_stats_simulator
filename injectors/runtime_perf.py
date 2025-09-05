#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from functools import wraps
from rich.console import Console

colored = Console()
_decorator_equal = "\n" + "[dim]=[/dim]" * 95

# ___________ timing | perf decorator:
def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        minutes, seconds = divmod(elapsed, 60)
        colored.print(_decorator_equal)
        colored.print(f"[bold][PERF STATS][/bold] for [bold green]{func.__name__:>25}[/bold green] | completed in: {int(minutes)}m {seconds:>5.2f}s ({elapsed:.4f} sec)\n")
        return result
    return wrapper

if __name__ == "__main__":
    pass