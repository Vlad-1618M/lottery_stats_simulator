## Sieve of Eratosthenes:
[sieve_eratosthenes_algo_prime_numbers.py](/math_modules/sieve_eratosthenes_algo_prime_numbers.py) script implements the Sieve of Eratosthenes algorithm to find prime numbers within a specified range:<br> 
It also provides an explanatory text about the algorithm, with optional translation into multiple languages using the AutoTranslator module:

### Features:
- Computes prime numbers between a start and end range using the Sieve of Eratosthenes:
- Supports CLI arguments for displaying algorithm explanation, listing available languages, or translating output:
- Provides a typewriter-style animated explanation with optional translation:
- Integrates with [AutoTranslator](/injectors/render_translit.py) for multilingual output:

### Dependencies:
- Python 3.11
- [rich](https://pypi.org/project/rich/)
- [render_translit.py](/injectors/render_translit.py)
- [time](https://docs.python.org/3/library/time.html) standard library, for typewriter effect:

### Example:
- Run the script with various CLI options to display primes, explanations, or supported languages:
- Lists primes from 0 to 11 (default range):
```bash
    python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py
    Primes from (0, 11): [2, 3, 5, 7, 11] 😎

    Parsed Args:
            --algo  : False
            --lang  : None
            --langs : False
```

#### CLI Examples:
- `--algo`  Sieve of Eratosthenes Algorithm Description:
- Displays the Sieve of Eratosthenes explanation:
```bash
 python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --algo
```
![--algo](/docs/png_docs/algo_description.png)

- `--langs` Lists available translation languages:
```bash
python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --langs
```
![--langs](/docs/png_docs/langs_arg.png)

- `--lang hy` Shows primes with `Armenian` translated labels:
- `--lang ar` Shows primes with `Arabic` translated labels:
- `--lang ru` Shows primes with `Russian` translated labels: 
- `--lang hi` Shows primes with `Hindi` translated labels:
- `--lang zh-CN` Shows primes with `Chinese` (simplified) translated labels:
- `--lang fr` Shows primes with `French` translated labels:
- `--lang iw` Shows primes with `Hebrew` translated labels:
---
- `--lang hy --algo` Sieve of Eratosthenes Algorithm Description translated to `Armenian`:
```bash
python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --lang hy --algo 
```
![--lang hy --algo](/docs/png_docs/lang_plus_algoi_in_Armenian.png)

- `--lang ar --algo` Sieve of Eratosthenes Algorithm Description translated to `Arabic`:
```bash
python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --lang ar --algo
```
![--lang ar --algo](/docs/png_docs/lang_plus_algo_in_Arabic.png)

- `--lang ru --algo` Sieve of Eratosthenes Algorithm Description translated to `Russian`:
```bash
python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --lang ru --algo 
```
![--lang ru --algo](/docs/png_docs/lang_plus_algo_in_Russian.png)

- `--lang hi --algo` Sieve of Eratosthenes Algorithm Description translated to `Hindi`:
```bash
python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --lang hi --algo 
```
![--lang hi --algo](/docs/png_docs/lang_plus_algo_in_Hinid.png)

- `--lang zh-CN --algo` Sieve of Eratosthenes Algorithm Description translated to `Chinese` (simplified):
```bash
python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --lang zh-CN --algo 
```
![--lang zh-CN --algo](/docs/png_docs/lang_plus_algo_in_Chinee.png)

- `--lang fr --algo` Sieve of Eratosthenes Algorithm Description translated to `French`:
```bash
python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --lang fr --algo
```
![--lang fr --algo](/docs/png_docs/lang_plus_algo_in_Franch.png)

- `--lang iw --algo` Sieve of Eratosthenes Algorithm Description translated to `Hebrew`:
```bash
python3 math_modules/sieve_eratosthenes_algo_prime_numbers.py --lang iw --algo 
```
![--lang iw --algo](/docs/png_docs/lang_plus_algo_in_Hebrew.png)

#### Function Description:

sieve_primes(start, end):
Returns a list of primes between start and end using the Sieve of Eratosthenes:
```python
def sieve_primes(start: int, end: int) -> list[int]:
    if end < 2:
        return []
    start = max(start, 2)
    sieve = [True] * (end + 1)
    sieve[:2] = [False, False]

    for num in range(2, int(end ** 0.5) + 1):
        if sieve[num]:
            sieve[num * num:end + 1: num] = [False] * len(range(num * num, end + 1, num))
    return [_ for _ in range(start, end + 1) if sieve[_]]
```

- sieve_explanation(translator=None):
- Prints a detailed explanation of the algorithm, optionally translated:
```python
def sieve_explanation(translator=None):
    explanation = (
        "\nSieve of Eratosthenes:\n"
        "The Sieve of Eratosthenes is a simple, ancient method for finding all primes up to a specific limit, ... almost like a filtering process hence the name Sieve:\n\n"
        "How it works or Calculation Method:\n\n"
        "Start with a list: Imagine you have a list of all numbers from 2 up to your chosen limit:\n"
        "Identify the very first primes.\n\n"
        "In mathematics, the number 2 is considered the starting number in calculation of the following sequence of primes, ... meaning the very first and smallest prime number is a number 2\n"
        "Mark its multipliers: Go through your list and cross out (or mark as composite) all multiples of 2 (4, 6, 8, 10, etc.). These numbers can't be primes because they're divisible by 2\n"
        "Move to the next number in your list that hasn't been crossed out. This number will be the next value in the list (in this case, 3)\n"
        "Mark its multiples: Now, cross out all multiples of 3 (6, 9, 12, 15, etc.). Some of these might already be crossed out (like 6), and that's perfectly acceptable:\n"
        "Repeat or continue this process: find the next unused number, declare it a one of primes, and then cross out all of its multiples:\n"
        "Once you've done this, for all numbers up to the square root of your list, any numbers remaining on your list which have not been used yet, are the primes!\n\n"
        "The core idea is that:\nInstead of checking each number individually to see if it's divisible by primes, the sieve efficiently eliminates multiples of known primes.\nThis means, that the Sieve of Eratosthenes is proactively removes composite numbers, leaving only primes.\n\n"
        "A primes (or a primes number) is a natural number which is greater than 1 that is not a result of a two smaller, natural numbers:\n"
        "A natural number, which is greater than 1 that is not a primes - is called a composite number:\n"
        " For example, 5 is a primes number, because the only way of writing its final result is: (1 × 5) or (5 × 1) where the 5 involvs itself.\n"
        " However, 4, is composite because its result of (2 × 2) in which both numbers are smaller than 4.\n\n"
        "Primes are central in number theory because of the fundamental theorem of arithmetic:\nevery natural number greater than 1, is either a primes by itself, or can be factorized as a result of primes that is unique up to their order:\n"
        "One of the main benefits using The Sieve of Eratosthenes, is that it may be used to find primes in arithmetic progressions:\n"
        "\nFor more info: See:\n -> [ https://www.britannica.com/science/number-theory ]"
        "\n -> [ https://math.libretexts.org/Courses/Coalinga_College/Math_for_Educators_(MATH_010A_and_010B_CID120)/04%3A_Number_Theory/4.03%3A_The_Sieve_of_Eratosthenes ]"
    )

    if translator:
        explanation = translator.translate(explanation)
    for char in explanation:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.003)
    print()

```
- run_primes(sequence_range, translit=False, lang=""):
- Computes and displays primes for a given range, with optional translation:
```python
def run_primes(sequence_range: tuple, translit=False, lang=""):
    if not isinstance(sequence_range, tuple):
        colored.print(f"\n... sequence integer [bold red]range[/bold red] in [bold]{__name__}.run_prime[/bold] function call is expected:")
        sys.exit("")

    primes = sieve_primes(*sequence_range)

    if translit:
        if not lang:
            colored.print("\n[bold red]Error:[/bold red] 'lang' parameter as 'language' must be specified when 'translit=[bold cyan]True'[/bold cyan]")
            return

        catalog = AutoTranslator.available_languages(as_dict=True)
        lang_code = (lang if lang in catalog else next((code for code, name in catalog.items() if name.lower() == lang.lower() or code == lang), None))

        if not lang_code:
            colored.print(f"[bold red]Error:[/bold red] Language '{lang}' not supported.")
            return

        try:
            translator = AutoTranslator(language=lang_code)
            title_text = translator.translate("Primes From")
            label_text = translator.translate(f"A mathematical range of composite number sequence {sequence_range} for the Primes Calculations: ")

            colored.rule(f"[bold green]{title_text} {sequence_range} (Translated to {lang_code.capitalize()})[/bold green]")
            colored.print(f"\n{label_text} [bold]{primes}[/bold] {be_cool}")
            return  # <-- print off | see default English version below:

        except Exception as e:
            colored.print(f"[bold red]Translation Failed:[/bold red] {str(e)}")
```
external_calls(args=None)
Allows external scripts to invoke the module with CLI-like arguments:
```python
def external_calls(args=None):
    """
    Allows external scripts to invoke this module's logic by passing args as a list.
        Example:
            external_calls(["--lang", "fr"])
            external_calls(["--algo"])
            external_calls(["--langs"])"""
    parser = argparse.ArgumentParser(description="Sieve of Eratosthenes explanation and prime number listing")
    parser.add_argument("--algo", action="store_true", help="Show algorithm explanation")
    parser.add_argument("--lang", type=str, help="Language code or name for translation")
    parser.add_argument("--langs", action="store_true", help="List available languages")

    parsed_args = parser.parse_args(args or [])
    main(optional_args=True, translator=None, lang_code=None, default_main_sequence=(0, 10), args=parsed_args)
```
- main(optional_args=False, translator=None, lang_code=None, default_main_sequence=(0, 10), args=None):
- Handles CLI arguments and executes the appropriate logic:
```python
def main(optional_args=False, translator=None, lang_code=None, default_main_sequence=(0, 10), args=None):
    if args is None:
        parser = argparse.ArgumentParser(description="Sieve of Eratosthenes explanation and prime number listing")
        parser.add_argument("--algo", action="store_true", help="Show algorithm explanation")
        parser.add_argument("--lang", type=str, help="Language code or name for translation")
        parser.add_argument("--langs", action="store_true", help="List available languages")
        args = parser.parse_args()

    # ____ handle (--langs) arg first | show available language list:
    if args.langs:
        colored.print("\n[bold]Available Languages:[/bold]\n")
        catalog = AutoTranslator.available_languages(as_dict=True)
        for code, name in catalog.items():
            colored.print(f"[bold cyan]{name:<8}[/bold cyan][yellow] <- [/yellow][dim]{code:>21}[/dim]")
        sys.exit(0)

    # ____ if language is specified | init translator api:
    if args.lang:
        catalog = AutoTranslator.available_languages(as_dict=True)
        lang_code = (args.lang if args.lang in catalog else next((code for code, name in catalog.items() if name.lower() == args.lang.lower()), None))

        if not lang_code:
            colored.print(f"\n[red]Invalid language:[/red] {args.lang}")
            sys.exit(1)
        translator = AutoTranslator(language=lang_code)
        run_primes(sequence_range=default_main_sequence, translit=True, lang=lang_code)

    # ____ output scenarios:
    if args.algo:
        # ___ show algorithm title first:
        algo_title = "Algorithm Description"
        if translator:
            algo_title = translator.translate(algo_title)
        colored.rule(f"[bold]'{algo_title}'[/bold]")
        sieve_explanation(translator)

    elif translator:
        # ___ show translated primes example:
        run_primes(sequence_range=default_main_sequence, translit=True, lang=lang_code)
    elif not any(vars(args).values()):
        # ___ if no args | show primes - decorative rules:
        primes = sieve_primes(*default_main_sequence)
        colored.print(f"\nPrimes from {default_main_sequence}: [bold]{primes}[/bold] {be_cool}")
    else:
        # ____ Default Case | normally shouldn't ge to this point:
        primes = sieve_primes(*default_main_sequence)
        colored.print(f"\nPrimes from {default_main_sequence}: [bold]{primes}[/bold] {be_cool}")

    if optional_args:
        colored.print("\n[bold yellow]Parsed Args:[/bold yellow]")
        for arg, val in vars(args).items():
            colored.print(f"\t[green]--{arg:<6}[/green]: [yellow]{val}[/yellow]")
```
#### Notes:
>- The `--algo` flag provides a detailed explanation with a typewriter effect (3ms delay per character):
>- Translation requires [render_translit.py](/injectors/render_translit.py) and valid language code or name `e.g.`, `fr` or `French`:
>- Pylint’s t`oo-complex` warning is disabled due to the script’s complex argument handling:

#### License:
- See LICENSE in the repository root for licensing details: