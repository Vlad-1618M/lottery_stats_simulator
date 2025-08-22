#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from rich.panel import Panel
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[0]))
from sieve_eratosthenes_algo_prime_numbers import sieve_primes
import number_generator

console = Console()


def get_primes_from_random(count: int, min_value: int, max_value: int, seed: int = None) -> tuple[list[int], list[int], int]:
    random_numbers = number_generator.generate_numbers_random(count, min_value, max_value, seed)
    prime_set = set(sieve_primes(start=min_value, end=max_value))
    primes_in_random = [num for num in random_numbers if num in prime_set]
    return random_numbers, primes_in_random, len(primes_in_random)


def main():
    numbers, any_primes, prime_count = get_primes_from_random(count=5, min_value=1, max_value=70, seed=None)
    print("\nRandom Numbers:\n", numbers)
    print("\nPrime Numbers Found:\n", any_primes)
    print(f"\nTotal Primes Found: {prime_count} out of {len(numbers)}")


def render_box():
    numbers, any_primes, prime_count = get_primes_from_random(count=5, min_value=1, max_value=70, seed=None)
    output_cleanp =  (
        ("Random Numbers:", f"\t[yellow]{', '.join(map(str, numbers)):>16}[/yellow]"),
        ("Primes Found:", f"\t[green]{', '.join(map(str, any_primes)):>16}[/green]"),
        (f"\n[green]{prime_count}[/green]", f"[dim]Primes found:[/dim][white] out of[/white] [yellow]{len(numbers)}[/yellow]"))

    result = "\n".join(f"{label} {value}" if isinstance(label, str) and isinstance(value, str) else label for (label, value) in output_cleanp)
    console.print(Panel(f"[bold]{result}[/bold]", title="Prime Number Roll"))


if __name__ == "__main__":
    render_box()
