#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import numpy as np
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from math_modules import sieve_eratosthenes_algo_prime_numbers as algo


def generate_numbers_np(count: int, min_value: int, max_value: int, seed: int = None) -> list[int]:
    if seed is not None:
        np.random.seed(seed)
    return np.random.randint(min_value, max_value + 1, size=count).tolist()


def get_primes_from_random(count: int, min_value: int, max_value: int, seed: int = None) -> tuple[list[int], list[int], int]:
    random_numbers = generate_numbers_random(count, min_value, max_value, seed)
    prime_set = set(algo.sieve_primes(start=min_value, end=max_value))
    primes_in_random = [num for num in random_numbers if num in prime_set]
    return random_numbers, primes_in_random, len(primes_in_random)


def main():
    numbers, any_primes, prime_count = get_primes_from_random(count=5, min_value=1, max_value=70, seed=None)
    print("\nRandom Numbers:\n", numbers)
    print("\nPrime Numbers Found:\n", any_primes)
    print(f"\nTotal Primes Found: {prime_count} out of {len(numbers)}")


def generate_numbers_random(count: int, min_value: int, max_value: int, seed: int = None) -> list[int]:
    results = set()
    if seed is not None:
        random.seed(seed)

    while len(results) < count:
        nums = random.randint(min_value, max_value)
        results.add(nums)
    return list(results)
    # return [random.randint(min_value, max_value) for _ in range(count)]


if __name__ == "__main__":
    main()

    # print(generate_numbers_np(count=5, min_value=1, max_value=70, seed=None))
    # print(generate_numbers_random(count=5, min_value=1, max_value=70, seed=None))
    # print(generate_numbers_random(count=20, min_value=1, max_value=70, seed=None))
