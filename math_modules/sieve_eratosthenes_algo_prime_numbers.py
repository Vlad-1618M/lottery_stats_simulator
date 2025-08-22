#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=too-complex

import sys
import argparse
from pathlib import Path
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
from injectors.render_translit import AutoTranslator
from time import sleep

colored = Console()
be_cool = "😎"

# ____ Prints a detailed explanation of the algorithm, optionally translated:
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

# ____ Returns a list of primes between start and end using the Sieve of Eratosthenes:
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


# ____ Computes primes for a given range, with optional translation:
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

# ___ for external scripts to call with CLI-like arguments:
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


# ___ cli args logic:
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

        # ___ show the primes example call:
        # colored.print(f"\nPrimes from {default_main_sequence}: [bold]{sieve_primes(*default_main_sequence)}[/bold] {be_cool}")
        # run_primes(sequence_range=default_main_sequence, translit=bool(translator), lang=lang_code)

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


if __name__ == "__main__":
    main(default_main_sequence=(0, 11), optional_args=True)
    
    # main(optional_args=False, translator=None, lang_code=None, default_main_sequence=(0, 100))
    # main(optional_args=False, translator=None, lang_code=None, default_main_sequence=(0, 100000))
    #  __________________ debug _________________
    # lang="de"
    # lang="iw"
    # lang="ar"
    # lang="uk"
    # lang="ru"
    # run_primes(sequence_range=(0, 10), translit=True, lang=lang)
    # catalog = AutoTranslator.available_languages(as_dict=True)
    # lang_code = (lang if lang in catalog else next((code for code, name in catalog.items() if name.lower() == lang.lower()), None))
    # lang_code = (lang if lang in catalog else next((code for code, name in catalog.items() if name.lower() == lang.lower() or code == lang), None))
    # print(lang_code)
