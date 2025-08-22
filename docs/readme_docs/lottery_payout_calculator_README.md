# Lottery Payout Calculator:
[payout.py](/math_modules/payout.py) script calculates federal and state tax withholdings for lottery winnings:<br> 
Supporting both `lump sum` and `annuity` payout options:<br> 
Provides detailed output with rich library colorized formatting for Powerball, Mega Millions, and custom jackpot amounts:

### Features:
- Calculates lump sum or annuity payouts with federal (24%) and state tax withholdings:
- Supports state-specific tax rates and special cases (e.g., California, New York):
- Provides CLI interface for specifying game, amount, cash option, state, and annuity years:
- Displays explanatory notes on lottery tax rules:
- CLI argument parsing with dynamic script name handling included:

### Dependencies:
- Python 3.11
- [rich](https://pypi.org/project/rich/):
- [shlex](https://docs.python.org/3/library/shlex.html) (standard library, for CLI help notes around string construction):
---
### CLI Call Example & Command Description:
```bash
python3 math_modules/payout.py --amount 500000000

Annuity Mode over 30 years for $ 500,000,000.00 if/as advertised:
Annual Gross Payment:           -> $ 16,666,666.67
-------------------------------------------------------
Annual Withholding:
        Federal 24 %            -> $ 4,000,000.00
        State Tax:              -> $ 0.00
        Total Withheld:         -> $ 4,000,000.00
        Net Pay:                -> $ 12,666,666.67
-------------------------------------------------------
Total Over 30 years:
Federal Withheld:               -> $ 120,000,000.00
State Tax:                      -> $ 0.00

Total Withheld:                 -> $ 120,000,000.00
Total Net After All Tax Withholdings: = $ 380,000,000.00

No state cli argument was provided | assuming 0 % state tax:

Annuity mode:   Withholding / tax rates occur yearly: e.g 24% for federal + state rate:
                Final liability depends on your marginal bracket at filing:

-------------------------------------------------------
```
- Run the script with CLI arguments to calculate lottery payouts:
```bash
python3 math_modules/payout.py --help
usage: payout.py [-h] [--game {lotto,megamillions,powerball}] [--amount AMOUNT] [--cash-option CASH_OPTION] [--annuity] [--years YEARS] [--state STATE] [--ticket-state TICKET_STATE] [--state-rate STATE_RATE] [--info]

Approximate federal + state withholding for lottery jackpots (lump sum or annuity).

options:
  -h, --help            show this help message and exit
  --game {lotto,megamillions,powerball}
                        Game to calculate (ignored if --amount provided).
  --amount AMOUNT       Custom jackpot amount in dollars (overrides --game).
  --cash-option CASH_OPTION
                        Fraction of jackpot for lump sum (e.g., 0.52). If omitted, annuity assumed.
  --annuity             Force annuity mode (use with --years).
  --years YEARS         Annuity years (default: 30).
  --state STATE         Two-letter code or full state name (participant in Powerball/Mega Millions).
  --ticket-state TICKET_STATE
                        State where ticket was purchased (matters for CA).
  --state-rate STATE_RATE
                        Override state tax rate as decimal (e.g., 0.0495 for 4.95%).
  --info                Show explanatory notes and exit.

˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙
CLI args call examples:

        Lump sum: | IL flat tax:
        python3 payout.py --game powerball --cash-option 0.52 --state IL

        Lump sum: | CA winner with CA ticket | 0% CA tax:
        python3 payout.py --amount 500000000 --cash-option 0.6 --state CA --ticket-state CA

        Lump sum: | CA resident with NV ticket | warn + suggest rate:
        python3 payout.py --game megamillions --cash-option 0.6 --state CA --ticket-state NV

        Annuity:  | 30 yrs | NY resident | warn to pass rate:
        python3 payout.py --game powerball --annuity --state NY --years 30

        Lump sum: | PA with explicit state rate of 3.07%
        python3 payout.py --amount 300000000 --cash-option 0.52 --state PA --state-rate 0.0307

        Show explanatory notes:
        python3 payout.py --info

```
- Lump sum for Powerball with Illinois tax:
- `--game powerball --cash-option 0.52 --state IL`
```bash
ython3 math_modules/payout.py --game powerball --cash-option 0.52 --state IL

Lump Sum Mode: --> cash option 52% of $ 526,000,000.00 if/as advertised:
Estimated Cash Value: = $ 273,520,000.00
-------------------------------------------------------
Initial Tax Withholdings:
        Federal 24 %            ->  $ 65,644,800.00
        IL state tax:           ->  $ 13,539,240.00
        Total Withheld:         ->  $ 79,184,040.00
-------------------------------------------------------
Net After Withholding:          ->  $ 194,335,960.00
Note: --> The 24% federal is initial withholding:
          Actual federal liability may go up to ~37% depending on income or shortfall due at filing:
```

- Lump sum for $500M with no CA tax:
- `--amount 500000000 --cash-option 0.6 --state CA --ticket-state CA`
```bash
python3 math_modules/payout.py --amount 500000000 --cash-option 0.6 --state CA --ticket-state CA

Lump Sum Mode: --> cash option 60% of $ 500,000,000.00 if/as advertised:
Estimated Cash Value: = $ 300,000,000.00
-------------------------------------------------------
Initial Tax Withholdings:
        Federal 24 %            ->  $ 72,000,000.00
        CA state tax:           ->  $ 0.00
        Total Withheld:         ->  $ 72,000,000.00
-------------------------------------------------------
Net After Withholding:          ->  $ 228,000,000.00
Note: --> The 24% federal is initial withholding:
          Actual federal liability may go up to ~37% depending on income or shortfall due at filing:
```

- Lump sum for Mega Millions, CA resident, NV ticket:
- `--game megamillions --cash-option 0.6 --state CA --ticket-state NV`
```bash
python3 math_modules/payout.py --game megamillions --cash-option 0.6 --state CA --ticket-state NV

Lump Sum Mode: --> cash option 60% of $ 198,000,000.00 if/as advertised:
Estimated Cash Value: = $ 118,800,000.00
-------------------------------------------------------
Initial Tax Withholdings:
        Federal 24 %            ->  $ 28,512,000.00
        CA state tax:           ->  $ 0.00
        Total Withheld:         ->  $ 28,512,000.00
-------------------------------------------------------
Net After Withholding:          ->  $ 90,288,000.00
CA resident + non-CA ticket: California taxes out-of-state lottery winnings. Use --state-rate (e.g., 0.093).
Note: --> The 24% federal is initial withholding:
          Actual federal liability may go up to ~37% depending on income or shortfall due at filing:
```

- Annuity for Powerball with NY tax warning:
- `--game powerball --annuity --state NY --years 30`
```bash
python3 math_modules/payout.py --game powerball --annuity --state NY --years 30

Annuity Mode over 30 years for $ 526,000,000.00 if/as advertised:
Annual Gross Payment:           -> $ 17,533,333.33
-------------------------------------------------------
Annual Withholding:
        Federal 24 %            -> $ 4,208,000.00
        NY state tax:           -> $ 0.00
        Total Withheld:         -> $ 4,208,000.00
        Net Pay:                -> $ 13,325,333.33
-------------------------------------------------------
Total Over 30 years:
Federal Withheld:               -> $ 126,240,000.00
State Tax:                      -> $ 0.00

Total Withheld:                 -> $ 126,240,000.00
Total Net After All Tax Withholdings: = $ 399,760,000.00
NY has progressive state (and possible NYC/Yonkers) taxes. Pass --state-rate (e.g., 0.109).

Annuity mode:   Withholding / tax rates occur yearly: e.g 24% for federal + state rate:
                Final liability depends on your marginal bracket at filing:

-------------------------------------------------------
```
- Show explanatory notes on how the lottery winnings are calculated and taxed:
- `--info`
```bash
python3 math_modules/payout.py --info

How Lottery Winnings Are Calculated and Taxed:
---------------------------------------------------------------------------
 
 • Lottery winnings are taxable income, taxed like wages at your marginal rate:
   24% federal withholding applies, but actual tax may be higher (up to 37%):
   More info:   ->  https://www.irs.gov/taxtopics/tc419

 • Winnings over $ 5,000 trigger Form W-2G with 24% federal withholding:
   More info:   ->  https://www.hrblock.com/tax-center/income/lottery-tax-calculator/

 • Federal tax brackets (2025): 10% to 37%; large winnings often hit 37%:
   Info:        ->  https://taxfoundation.org/data/all/federal/2025-tax-brackets/

 • State taxes vary; some states (e.g., CA, TX) have no income tax, others (e.g., NY) exceed 10%:
   Article:     ->  https://people.com/powerball-jackpot-lottery-hits-426-million-how-much-would-winner-get-taxes-11784570

 • Report winnings on Form 1040, Schedule 1:
   More info:   ->  https://www.irs.gov/taxtopics/tc419

 • Consult a tax advisor for large winnings to explore annuities, gifting, or charitable options:
   Tips:        ->  https://www.kiplinger.com/taxes/603033/tax-tips-for-gambling-winnings-and-losses
```

#### Function Description:
- `info():`
- Returns explanatory notes on lottery tax calculations:
```python
def info():
    """Display explanatory notes about lottery tax calculations."""
    decor = "-" * 75
    dot = "[bright_yellow]•[/bright_yellow]"
    arrow = "[orange1]-> [/orange1]"
    _ = "[bright_green]$ [/bright_green]"
    return (
        f"\nHow Lottery Winnings Are Calculated and Taxed:\n{decor}\n"
        f" \n {dot} Lottery winnings are taxable income, taxed like wages at your marginal rate:\n"
        f"   24% federal withholding applies, but actual tax may be higher (up to 37%):\n"
        f"   [dim]More info[/dim]:\t{arrow} [bright_cyan]https://www.irs.gov/taxtopics/tc419[/bright_cyan]\n"
        f"\n {dot} Winnings over {_}5,000 trigger Form W-2G with 24% federal withholding:\n"
        f"   [dim]More info[/dim]:\t{arrow} [bright_cyan]https://www.hrblock.com/tax-center/income/lottery-tax-calculator/[/bright_cyan]\n"
        f"\n {dot} Federal tax brackets (2025): 10% to 37%; large winnings often hit 37%:\n"
        f"   [dim]Info[/dim]:\t{arrow} [bright_cyan]https://taxfoundation.org/data/all/federal/2025-tax-brackets/[/bright_cyan]\n"
        f"\n {dot} State taxes vary; some states (e.g., CA, TX) have no income tax, others (e.g., NY) exceed 10%:\n"
        f"   [dim]Article[/dim]:\t{arrow} [bright_cyan]https://people.com/powerball-jackpot-lottery-hits-426-million-how-much-would-winner-get-taxes-11784570[/bright_cyan]\n"
        f"\n {dot} Report winnings on Form 1040, Schedule 1:\n"
        f"   [dim]More info[/dim]:\t{arrow} [bright_cyan]https://www.irs.gov/taxtopics/tc419[/bright_cyan]\n"
        f"\n {dot} Consult a tax advisor for large winnings to explore annuities, gifting, or charitable options:\n"
        f"   [dim]Tips[/dim]:\t{arrow} [bright_cyan]https://www.kiplinger.com/taxes/603033/tax-tips-for-gambling-winnings-and-losses[/bright_cyan]\n"
    )
        # _____________ Note: ref URLs may change:
```
- `normalize_state(state):`
- Converts state input to a two-letter code, raising an error for invalid states.
```python
def normalize_state(state):
    """Normalize state input to two-letter code."""
    if not state:
        return None
    state = state.strip().lower()
    if len(state) == 2:
        return state.upper()
    if state not in CONFIG["name_to_code"]:
        raise ValueError(f"Invalid state name: {state}")
    return CONFIG["name_to_code"][state]

```
- `resolve_state_rate(state_code, ticket_state_code, override_rate)`
- Determines state tax rate:
```python
def resolve_state_rate(state_code, ticket_state_code, override_rate):
    """Determine state tax rate and any associated note."""
    if override_rate is not None:
        if not 0 <= override_rate <= 1:
            raise ValueError("State tax rate must be between 0 and 1")
        return override_rate, None

    if not state_code:
        return 0.0, "\n[red]No[/red] state [dim]cli argument[/dim] was provided | assuming [bold]0[/bold] [bold red]%[/bold red] state tax:"

    if state_code == "CA":
        if ticket_state_code in (None, "CA"):
            return 0.0, None
        return 0.0, ("[yellow]CA resident + non-CA ticket: California taxes out-of-state lottery winnings. "
                     "Use --state-rate (e.g., 0.093).[/yellow]")

    if state_code in CONFIG["state_tax_rates"]:
        return CONFIG["state_tax_rates"][state_code], None

    if state_code == "NY":
        return 0.0, ("[yellow]NY has progressive state (and possible NYC/Yonkers) taxes. "
                     "Pass --state-rate (e.g., 0.109).[/yellow]")

    if state_code == "PA":
        return 0.0, ("[yellow]PA taxes lottery winnings (e.g., 3.07%). "
                     "Pass --state-rate (e.g., 0.0307).[/yellow]")

    return 0.0, ("[yellow]State tax treatment varies (progressive/local). "
                 "Pass --state-rate to override default 0%.[/yellow]")
```
- `calculate_lump_sum(jackpot_amount, cash_option, state_rate)`
- Calculates lump sum payout with tax withholdings:

```python
def calculate_lump_sum(jackpot_amount, cash_option, state_rate):
    """Calculate lump sum payout with tax withholdings."""
    if jackpot_amount <= 0:
        raise ValueError("Jackpot amount must be positive")
    if not 0 < cash_option <= 1:
        raise ValueError("Cash option must be between 0 and 1")

    cash_value = jackpot_amount * cash_option
    federal_withholding = cash_value * CONFIG["federal_withholding"]
    state_tax = cash_value * state_rate
    total_withheld = federal_withholding + state_tax
    net_after_withholding = cash_value - total_withheld

    note = ("[bold]Note[/bold]: [dim]--> The[/dim] [bold red]24%[/bold red] [dim]federal is initial withholding[/dim]:"
            "\n\t  [dim]Actual federal liability may go up to[/dim] [bold red]~37%[/bold red] [dim]depending on income or shortfall due at filing[/dim]:")

    return {
        "mode": "lump_sum",
        "jackpot_amount": jackpot_amount,
        "cash_option": cash_option,
        "cash_value": cash_value,
        "federal_withholding_amount": federal_withholding,
        "state_tax_amount": state_tax,
        "total_initial_withholding": total_withheld,
        "net_after_withholding": net_after_withholding,
        "note": note,
    }
```
- `calculate_annuity(jackpot_amount, years, state_rate`)
- Calculates annuity payout over specified years with withholdings:

```python
def calculate_annuity(jackpot_amount, years, state_rate):
    """Calculate annuity payout with tax withholdings."""
    if jackpot_amount <= 0:
        raise ValueError("Jackpot amount must be positive")
    if years <= 0:
        raise ValueError("Annuity years must be positive")

    annual_gross = jackpot_amount / years
    annual_federal = annual_gross * CONFIG["federal_withholding"]
    annual_state = annual_gross * state_rate
    annual_withheld = annual_federal + annual_state
    annual_net = annual_gross - annual_withheld

    total_federal = annual_federal * years
    total_state = annual_state * years
    total_withheld = annual_withheld * years
    total_net = annual_net * years    
    
    note = ("\nAnnuity mode:\t[bold]Withholding[/bold] / [bold]tax rates[/bold] occur yearly: "
            "[dim]e.g[/dim] [bold]24[/bold][bold red]%[/bold red] for [bold red]federal[/bold red] [dim]+[/dim] [bold yellow]state[/bold yellow] rate:"
            "\n\t\tFinal liability depends on your marginal bracket at filing:")

    return {
        "mode": "annuity",
        "jackpot_amount": jackpot_amount,
        "years": years,
        "annual_gross": annual_gross,
        "annual_federal_withholding": annual_federal,
        "annual_state_tax": annual_state,
        "annual_total_withheld": annual_withheld,
        "annual_net_after_withholding": annual_net,
        "total_federal_withholding": total_federal,
        "total_state_tax": total_state,
        "total_initial_withholding": total_withheld,
        "total_net_after_withholding": total_net,
        "note": note,
    }
```
- `gfx_decor():`
- Returns formatting strings for styled console output:
```python
def gfx_decor():
    """Return formatting strings for output."""
    return {
        "dollar": "[bright_green]$ [/bright_green]",
        "arrow": "\t\t[dim]->[/dim] ",
        "line": "[dim]-[/dim]" * 55,
        "yearly": "[bright_green]Annual[/bright_green] Withholding:",
        "yearly_gross": "Annual [bright_green]Gross[/bright_green] Payment:",
        "annual_total": "\t[bright_red]Total Withheld[/bright_red]",
        "annual_net": "\t[bright_green]Net Pay[/bright_green]:",
        "federal": "\t[bold]Federal[/bold] [orange1]24 [bright_red]%[/bright_red][/orange1]",
        "state": "[bold red]State[/bold red] [bold]Tax[/bold]:\t",
        "total_federal": "[bold red]Federal[/bold red] Withheld:",
        "total_withheld": "\n[bold]Total[/bold] [bold red]Withheld[/bold red]:",
        "total_net_pay": "[bold]Total [bold green]Net[/bold green] After [bold red]All Tax Withholdings[/bold red][/bold]: [bold]=[/bold] ",
        "initial_tax_withholdings": "Initial [bold red]Tax Withholdings[/bold red]:",
        "estimated_cash_payout": "[bold green]Estimated[/bold green] Cash Value:",
    }
```
- `print_summary(summary, state_label, state_note)`
- Prints formatted payout details for lump sum / annuity:
```python
def print_summary(summary, state_label, state_note):
    """Print calculation summary for lump sum or annuity."""
    render_styles = gfx_decor()
    if summary["mode"] == "lump_sum":
        colored.print(f"\n[bold cyan]Lump Sum Mode[/bold cyan]: --> [bold green]cash option[/bold green] [bold red]{summary['cash_option']:.0%}[/bold red] "
                     f"of {render_styles['dollar']}{summary['jackpot_amount']:,.2f} [dim]if/as [/dim]advertised:")
        colored.print(f"{render_styles['estimated_cash_payout']} [bold]=[/bold] {render_styles['dollar']}[red]{summary['cash_value']:,.2f}[/red]")
        colored.print(f"{render_styles['line']}")
        colored.print(f"{render_styles['initial_tax_withholdings']}")
        colored.print(f"{render_styles['federal']}{render_styles['arrow']} {render_styles['dollar']}{summary['federal_withholding_amount']:,.2f}")
        colored.print(f"\t{(state_label or render_styles['state'])}:{render_styles['arrow']} {render_styles['dollar']}{summary['state_tax_amount']:,.2f}")
        colored.print(f"{render_styles['annual_total']}:{render_styles['arrow']} {render_styles['dollar']}{summary['total_initial_withholding']:,.2f}")
        colored.print(f"{render_styles['line']}")
        colored.print(f"[bold green]Net[/bold green] After [bold red]Withholding[/bold red]:{render_styles['arrow']} "
                     f"[bold red]$[/bold red][bold green] {summary['net_after_withholding']:,.2f}[/bold green]")
    else:
        colored.print(f"\n[bright_yellow]Annuity Mode[/bright_yellow] [dim]over[/dim] [bright_white]{summary['years']}[/bright_white] "
                     f"[dim]years[/dim] for {render_styles['dollar']}[bold]{summary['jackpot_amount']:,.2f}[/bold] [dim]if/as [/dim]advertised:")
        colored.print(f"{render_styles['yearly_gross']}{render_styles['arrow']}{render_styles['dollar']}{summary['annual_gross']:,.2f}")
        colored.print(f"{render_styles['line']}")
        colored.print(f"{render_styles['yearly']}")
        colored.print(f"{render_styles['federal']}{render_styles['arrow']}{render_styles['dollar']}{summary['annual_federal_withholding']:,.2f}")
        colored.print(f"\t{(state_label or render_styles['state'])}:{render_styles['arrow']}{render_styles['dollar']}{summary['annual_state_tax']:,.2f}")
        colored.print(f"{render_styles['annual_total']}:{render_styles['arrow']}{render_styles['dollar']}{summary['annual_total_withheld']:,.2f}")
        colored.print(f"{render_styles['annual_net']}{render_styles['arrow']}{render_styles['dollar']}{summary['annual_net_after_withholding']:,.2f}")
        colored.print(f"{render_styles['line']}")
        colored.print(f"[bright_yellow]Total Over [bold cyan]{summary['years']}[/bold cyan] years[/bright_yellow]:")
        colored.print(f"{render_styles['total_federal']}{render_styles['arrow']}{render_styles['dollar']}{summary['total_federal_withholding']:,.2f}")
        colored.print(f"{render_styles['state']}{render_styles['arrow']}{render_styles['dollar']}{summary['total_state_tax']:,.2f}")
        colored.print(f"{render_styles['total_withheld']}\t{render_styles['arrow']}{render_styles['dollar']}{summary['total_initial_withholding']:,.2f}")
        colored.print(f"{render_styles['total_net_pay']}[bold red]$[/bold red][bold green] {summary['total_net_after_withholding']:,.2f}[/bold green]")

    if state_note:
        colored.print(state_note)
    colored.print(f"{summary['note']}\n")
    colored.print(f"{render_styles['line']}")
```
- `build_parser():`
- CLI argument parser with dynamic script name:
```python
def build_parser():
    call_name = ' '.join(map(shlex.quote, (os.path.basename(sys.executable), os.path.basename(sys.argv[0]))))
    examples = f"""

˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙
CLI args call examples:\n
  \tLump sum: | IL flat tax:
  \t{call_name} --game powerball --cash-option 0.52 --state IL

  \tLump sum: | CA winner with CA ticket | 0% CA tax:
  \t{call_name} --amount 500000000 --cash-option 0.6 --state CA --ticket-state CA

  \tLump sum: | CA resident with NV ticket | warn + suggest rate:
  \t{call_name} --game megamillions --cash-option 0.6 --state CA --ticket-state NV

  \tAnnuity:  | 30 yrs | NY resident | warn to pass rate:
  \t{call_name} --game powerball --annuity --state NY --years 30

  \tLump sum: | PA with explicit state rate of 3.07%
  \t{call_name} --amount 300000000 --cash-option 0.52 --state PA --state-rate 0.0307

  \tShow explanatory notes:
  \t{call_name} --info
"""
    parser = argparse.ArgumentParser(description="Approximate federal + state withholding for lottery jackpots (lump sum or annuity).", epilog=examples, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--game", choices=sorted(CONFIG["jackpots"].keys()), help="Game to calculate (ignored if --amount provided).")
    parser.add_argument("--amount", type=float, help="Custom jackpot amount in dollars (overrides --game).")
    parser.add_argument("--cash-option", type=float, help="Fraction of jackpot for lump sum (e.g., 0.52). If omitted, annuity assumed.")
    parser.add_argument("--annuity", action="store_true", help="Force annuity mode (use with --years).")
    parser.add_argument("--years", type=int, default=CONFIG["default_years"], help=f"Annuity years (default: {CONFIG['default_years']}).")
    parser.add_argument("--state", help="Two-letter code or full state name (participant in Powerball/Mega Millions).")
    parser.add_argument("--ticket-state", help="State where ticket was purchased (matters for CA).")
    parser.add_argument("--state-rate", type=float, help="Override state tax rate as decimal (e.g., 0.0495 for 4.95%%).")
    parser.add_argument("--info", action="store_true", help="Show explanatory notes and exit.")
    return parser

```
- `pick_state_rate(args)`
- Resolves state tax rate and label based on CLI arguments:
```python
def pick_state_rate(args):
    """Determine state tax rate, note, and label."""
    state = normalize_state(args.state)
    ticket_state = normalize_state(args.ticket_state)

    if state and state not in CONFIG["participants"]:
        colored.print(f"State [bold red]{args.state}[/bold red] is not in [bold]Powerball/Mega Millions[/bold] participant list:")
        sys.exit(1)

    rate, note = resolve_state_rate(state, ticket_state, args.state_rate)
    state_label = f"{state} state tax" if state else "State Tax"
    return rate, note, state_label

```
- `main():`
- Processes CLI arguments and executes payout calculations:
```python
def main():
    """Main function to process CLI arguments and perform calculations."""
    parser = build_parser()
    args = parser.parse_args()

    if args.info:
        colored.print(info())
        return

    if args.amount is not None:
        if args.amount <= 0:
            parser.error("Jackpot amount must be positive")
        jackpot = args.amount
    elif args.game:
        jackpot = CONFIG["jackpots"][args.game]
    else:
        parser.error("Provide --game or --amount")

    if args.state_rate is not None and not (0 <= args.state_rate <= 1):
        parser.error("State tax rate must be between 0 and 1")

    state_rate, state_note, state_label = pick_state_rate(args)

    if args.cash_option is not None:
        summary = calculate_lump_sum(jackpot, args.cash_option, state_rate)
    else:
        if args.years <= 0:
            parser.error("Annuity years must be positive")
        summary = calculate_annuity(jackpot, args.years, state_rate)

    print_summary(summary, state_label, state_note)

```
#### Notes:
- Exampled Jackpot amounts are predefined for Powerball ($526M), Mega Millions ($198M), and Lotto ($13.85M) as of 2025 `e.g`, default values in the ***CONFIG["jackpots"]*** dictionary:
```python
CONFIG = {
    "jackpots": {
        "powerball": 526_000_000,
        "megamillions": 198_000_000,
        "lotto": 13_850_000,
    },
```
- However, the `--amount` CLI flag allows to override these with any positive float value: 
- Script checks for this in `main()` function: 
- if `--amount` is provided, it'll use that value: 
- else falls back to predefined game amounts:
```python
if args.amount is not None:
        if args.amount <= 0:
            parser.error("Jackpot amount must be positive")
        jackpot = args.amount
    elif args.game:
        jackpot = CONFIG["jackpots"][args.game]
    else:
        parser.error("Provide --game or --amount")
```

```bash
python3 math_modules/payout.py --amount 1000000 --cash-option 0.6 --state IL

Lump Sum Mode: --> cash option 60% of $ 1,000,000.00 if/as advertised:
Estimated Cash Value: = $ 600,000.00
-------------------------------------------------------
Initial Tax Withholdings:
        Federal 24 %            ->  $ 144,000.00
        IL state tax:           ->  $ 29,700.00
        Total Withheld:         ->  $ 173,700.00
-------------------------------------------------------
Net After Withholding:          ->  $ 426,300.00
Note: --> The 24% federal is initial withholding:
          Actual federal liability may go up to ~37% depending on income or shortfall due at filing:

-------------------------------------------------------

```
- Federal withholding is set at 24%, but actual liability may reach 37% (noted in output):
- State tax rates are included for select states; others require `--state-rate` for accuracy (e.g., NY, PA):
- The script uses shlex.quote for safe CLI example generation:
- URLs in `info()` may need periodic verification for validity:

### License:
- See LICENSE in the repository root for licensing details.
---
