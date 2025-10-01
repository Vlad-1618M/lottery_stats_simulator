#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import yaml
import signal
import platform
import argparse
from pathlib import Path
from rich.console import Console
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

console = Console()

arrow = "[bold green]→[/bold green]"
check = "[bright_green]✓ [/bright_green]"
_tab = "\t "

# ______ try for keyboard support | OS Arch depended | Mac needs fullpermission, so block it on macOS:
try:
    import keyboard
    if platform.system().lower() == "darwin":
        KEYBOARD_AVAILABLE = False  # disable on macOS
    else:
        KEYBOARD_AVAILABLE = True
except Exception:
    KEYBOARD_AVAILABLE = False

STOP_SESSION = False

def set_stop():
    global STOP_SESSION
    STOP_SESSION = True
    console.print(f"\n[bold red][EXIT][/bold red]: [bold magenta]Requested[/bold magenta]: {arrow} [dim]closing browser session[/dim]...")


def handle_sigint(sig, frame):
    set_stop()

signal.signal(signal.SIGINT, handle_sigint)


# ____________________ help functions:
def _safe_slug(subject_string: str) -> str:
    if not subject_string:
        return "untitled"
    prep_strings = subject_string.strip().strip("/ ")
    ready_string = re.sub(r"[^A-Za-z0-9._-]+", "_", prep_strings)
    return ready_string or "untitled"


def yaml_filename_from_url(url: str, outdir: Path) -> Path:
    parsed = urlparse(url)
    netloc = _safe_slug(parsed.netloc or "site")
    path_stem = _safe_slug(Path(parsed.path).stem or "index")
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir / f"{netloc}_{path_stem}.yml"


def dump_dom_to_yaml(page, outdir: str = "_mapped_dom_dump") -> dict:
    info = {
        "title": page.title(),
        "url": page.url,
        "links": page.eval_on_selector_all(
            "a",
            "els => els.map(e => ({ text: (e.innerText || '').trim(), href: e.href }))",
        ),
        "buttons": page.eval_on_selector_all(
            "button",
            "els => els.map(e => ({ text: (e.innerText || '').trim() }))",
        ),
    }
    outfile = yaml_filename_from_url(page.url, Path(outdir))
    outfile.write_text(yaml.safe_dump(info, sort_keys=False), encoding="utf-8")
    console.print(f"\n[dim][YAML[/dim]: [bold green]saved[/bold green]: {arrow} [bold magenta]{outfile}[/bold magenta]")
    return info


# ____________________ interactive mode:
def interactive_mode(start_url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome")
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        page.goto(start_url, wait_until="domcontentloaded")
        console.print(f"\n{check} [bright_green][Page Opened][/bright_green]: {arrow} [bright_cyan]{start_url}[/bright_cyan]")
        dom_info = dump_dom_to_yaml(page)
        elements = dom_info["links"] + dom_info["buttons"]

        if not elements:
            console.print("[bold red]No[/bold red] interactive elements found:")
            browser.close()
            return

        if KEYBOARD_AVAILABLE:
            console.print(f"\n[bold red][Interactive mode enabled][/bold red] {arrow} if on macOS [bold]Accessibility Permission[/bold] required:")
            console.print("\t[bright_yellow]↑[/bright_yellow] / [bright_blue]↓[/bright_blue] cycle through elements"
                          "\n\t[bold]Enter[/bold] to click"
                          "\n\t[bold red]Ctrl+X[/bold red]/C to exit\n")

            current_index = 0
            def show_current():
                item = elements[current_index]
                if "href" in item:
                    console.print(f"[{current_index:>3}] [bold orange1]Link[/bold orange1]: {arrow} [bold cyan italic]{item['text'] or '(no text)'} → {item['href']}[/bold cyan italic]")
                else:
                    console.print(f"[{current_index}] Button: {item['text'] or '(no label)'}")

            def on_up(_=None):
                # nonlocal here - is a scope directive for Python unlike module-level globals, but only works for variables in an enclosing/inner function:
                # nonlocal means: - when current_index is in use in this inner function, instead of new function create call, refer to the variable that lives in the nearest enclosing function: 
                nonlocal current_index
                current_index = (current_index - 1) % len(elements)
                show_current()

            def on_down(_=None):
                nonlocal current_index
                current_index = (current_index + 1) % len(elements)
                show_current()

            def on_enter(_=None):
                nonlocal current_index
                item = elements[current_index]
                if "href" in item and item["href"]:
                    console.print(f"Navigating → {item['href']}")
                    page.goto(item["href"], wait_until="domcontentloaded")
                else:
                    try:
                        page.get_by_role("button", name=item.get("text") or "", exact=False).first.click()
                    except Exception as e:
                        console.print("[action failed]:", e)

                new_info = dump_dom_to_yaml(page)
                elements[:] = new_info["links"] + new_info["buttons"]

            keyboard.on_press_key("up", lambda _: on_up())
            keyboard.on_press_key("down", lambda _: on_down())
            keyboard.on_press_key("enter", lambda _: on_enter())
            keyboard.add_hotkey("ctrl+x", set_stop)
            keyboard.add_hotkey("ctrl+c", set_stop)

            show_current()
            while not STOP_SESSION:
                page.wait_for_timeout(200)

        else:
            console.print("\n[Keyboard control unavailable — fallback mode]")
            for i, item in enumerate(elements, start=1):
                if "href" in item:
                    console.print(f"{i:2d}. Link: {item['text'] or '(no text)'} → {item['href']}")
                else:
                    console.print(f"{i:2d}. Button: {item['text'] or '(no label)'}")

            console.print("\nClose the browser manually when done.")
            page.wait_for_timeout(8000)

        browser.close()
        console.print("\n[bold]...[/bold] [dim]browser closed[/dim]:\n" + "[dim]=[/dim]" * 60)


def auto_scroll(page, step=300, delay=200, max_scroll=3000):
    current = 0
    while current < max_scroll:
        page.evaluate(f"window.scrollBy(0, {step})")
        page.wait_for_timeout(delay)
        current += step


# ____________________ page replay mode this is where the .yml cgf from interactive mode is in use - hence replay/re-run:
def replay_mode(yaml_file: str, slower: int = 0, scroll: int = 3000):
    with sync_playwright() as init_page:
        browser = init_page.chromium.launch(headless=False, channel="chrome")
        page = browser.new_page(viewport={"width": 1980, "height": 1300})

        data = yaml.safe_load(Path(yaml_file).read_text(encoding="utf-8"))
        console.print(f"\n{check} {os.path.basename(yaml_file)}")
    
        start_url = data["url"]
        page.goto(start_url, wait_until="domcontentloaded")
        if slower:
            page.wait_for_timeout(slower)
        auto_scroll(page, step=400, delay=300, max_scroll=scroll)
        console.print(f"{check}[bright_green] Session Started[/bright_green]: {arrow} [bright_yellow italic]{start_url}[/bright_yellow italic]\n")

        steps = data.get("links", []) + data.get("buttons", [])
        for idx_count, item in enumerate(steps):
            if STOP_SESSION:
                break
            try:
                if "href" in item and item["href"]:
                    console.print(f"{check}[Replay]: {idx_count:>3} {arrow} [bright_blue italic]{item['href']}[/bright_blue italic]")
                    page.goto(item["href"], wait_until="domcontentloaded")
                    if slower:
                        page.wait_for_timeout(slower)
                    auto_scroll(page, step=400, delay=300, max_scroll=scroll)
                else:
                    console.print(f"{check} [Step {idx_count:>3}] clicked: {arrow} [bright_yellow italic]{item.get('text') or '(no label)'}[/bright_yellow italic]")
                    page.get_by_role("button", name=item.get("text") or "", exact=False).first.click()
            except Exception as failed_href_sequence:
                console.print(f"{_tab} [[bright_red] Step Failed [/bright_red]]: {arrow}", failed_href_sequence)
            page.wait_for_timeout(1000)

        console.print("Replay finished. Close browser manually.")
        page.wait_for_timeout(5000)
        browser.close()


# ____________________ arg parsers:
def parse_time(value: str) -> int:
    # ___ human readble time conversions to milliseconds (500, 5s, 2m):
    value = str(value).strip().lower()
    if value.endswith("ms"):
        return int(value[:-2])
    elif value.endswith("s"):
        return int(float(value[:-1]) * 1000)
    elif value.endswith("m"):
        return int(float(value[:-1]) * 60_000)
    else:
        return int(value)


def parse_size(value: str) -> int:
    # ___ human readble px size conversions (3000, 5k):
    value = str(value).strip().lower()
    if value.endswith("k"):
        return int(float(value[:-1]) * 1000)
    return int(value)


# ____________________ main + args:
def main():
    parser = argparse.ArgumentParser(description="Playwright DOM recorder / replayer")
    parser.add_argument("--replay", help="Replay from a saved .yml file")
    parser.add_argument("--url", default="https://google.com", help="Start URL for interactive mode")
    parser.add_argument("--slow", type=parse_time, default=0, help="Delay between steps (e.g. 500, 5s, 2m; default=0)")
    parser.add_argument("--scroll", type=parse_size, default=3000, help="Max scroll depth per page in px (e.g. 3000, 5k)")
    args = parser.parse_args()
    
    if args.replay:
        replay_mode(args.replay, slower=args.slow, scroll=args.scroll)
    else:
        interactive_mode(args.url)
    

if __name__ == "__main__":
    main()
