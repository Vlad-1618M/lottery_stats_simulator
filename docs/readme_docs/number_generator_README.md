# Number Generator:
The [number_generator.py](/math_modules/number_generator.py) script generates random numbers within a specified range and identifies prime numbers among them with [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes) algorithm:<br> 
Supports two random number generation methods:<br> 
- 1 using `NumPy` for efficiency:
- 2 using `Python’s` random module for uniqueness:

### Features:
- Generates a specified count of random integers within a given range:
- Identifies prime numbers in the generated set using the [sieve eratosthenes algo](/math_modules/sieve_eratosthenes_algo_prime_numbers.py) module:
- Supports optional `seed` for reproducible results:
- Outputs random numbers + prime numbers found, and the count of primes:

### Dependencies
- Python 3.11
- [NumPy](https://numpy.org/install/) see [requirements.txt](/deps/requirements.txt)
- [sieve_eratosthenes_algo_prime_numbers.py](/math_modules/sieve_eratosthenes_algo_prime_numbers.py)

### Call Example:
- Run the script directly to generate 5 random numbers between 1 and 70, identify primes, and print the results:
- Example Output:
```bash
    python3 math_modules/number_generator.py
    
    Random Numbers:
    [34, 5, 27, 28, 30]

    Prime Numbers Found:
    [5]
    Total Primes Found: 1 out of 5
```
### Function Description:
***generate_numbers_np():***
- Generates count random integers between min_value and max_value using NumPy: 
- Optional seed for reproducibility.
```python
def generate_numbers_np(count: int, min_value: int, max_value: int, seed: int = None) -> list[int]:
    if seed is not None:
        np.random.seed(seed)
    return np.random.randint(min_value, max_value + 1, size=count).tolist()
```
***generate_numbers_random()***:
- Generates count unique random integers using random module:
- Ensures no duplicates via a set:
```python
def get_primes_from_random(count: int, min_value: int, max_value: int, seed: int = None) -> tuple[list[int], list[int], int]:
    random_numbers = generate_numbers_random(count, min_value, max_value, seed)
    prime_set = set(algo.sieve_primes(start=min_value, end=max_value))
    primes_in_random = [num for num in random_numbers if num in prime_set]
    return random_numbers, primes_in_random, len(primes_in_random)
```
***get_primes_from_random():***
- Generates random numbers and returns a tuple of all numbers, primes found, and prime count:
```python
def generate_numbers_random(count: int, min_value: int, max_value: int, seed: int = None) -> list[int]:
    results = set()
    if seed is not None:
        random.seed(seed)

    while len(results) < count:
        nums = random.randint(min_value, max_value)
        results.add(nums)
    return list(results)
```
***main()***:
- Executes the default logic:
- generating and printing random numbers and their primes:
```python
def main():
    numbers, any_primes, prime_count = get_primes_from_random(count=5, min_value=1, max_value=70, seed=None)
    print("\nRandom Numbers:\n", numbers)
    print("\nPrime Numbers Found:\n", any_primes)
    print(f"\nTotal Primes Found: {prime_count} out of {len(numbers)}")
```
#### Notes:
- The script uses `generate_numbers_random` in `get_primes_from_random` for unique numbers, but `generate_numbers_np` is available for faster generation, however may include duplicates:
- The commented-out line in `generate_numbers_random` offers an alternative non-unique generation method:

##### License:
- See LICENSE in the repository root for licensing details: