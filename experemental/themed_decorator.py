#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import webbrowser
import importlib.util
from time import sleep
from pyfiglet import Figlet
from rich.table import Table
from rich.console import Console

colored = Console()

# ---------------------------------------------------------------------------------
# | Font Name     | Description / Style    |
# | ------------- | ---------------------- |
# | `slant`       | Italic slanted text    |
# | `standard`    | The default            |
# | `big`         | Large and bold letters |
# | `block`       | Thick blocky text      |
# | `bubble`      | Rounded "bubble" style |
# | `digital`     | Like a digital clock   |
# | `doom`        | Old-school game font   |
# | `lean`        | Narrow slanted         |
# | `banner`      | Simple block banner    |
# | `3-d`         | 3D styled text         |
# | `3x5`         | Compact 3x5 characters |
# | `isometric1`  | Isometric cube style   |
# | `ogre`        | Heavy and brutal       |
# | `roman`       | Serif classic          |
# | `script`      | Cursive/script look    |
# | `speed`       | Sleek italic feel      |
# | `starwars`    | Sci-fi themed          |
# | `univers`     | Clean and balanced     |
# | `ansi_shadow` | Shadowed block         |
# | ______________________________________ |
#    possible choised --> 3d-ascii
# ________________________________________________________________________________

def inspect_lib(lib_name: str, open_url: bool = False):
    """Inspect a Python library: show metadata, path, and optionally open homepage."""

    colored.print(f"\nInspecting: [bold]{lib_name}[/bold]")
    run = subprocess.run(["pip", "show", lib_name], capture_output=True, text=True)

    if run.returncode != 0 or not run.stdout:
        colored.print(f"[✘] Library '{lib_name}' not found.\n")
        return

    metadata = {}
    colored.print("[bold yellow]Package Metadata Check:[/bold yellow] [bold]✔[/bold]\n")
    for line in run.stdout.strip().splitlines():
        colored.print(f"[bold]{line}[/bold]")
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()

    #____ output lib source location and info:
    spec = importlib.util.find_spec(lib_name)
    if spec and spec.origin:
        colored.print(f"\n[bold yellow]Installed[/bold yellow] at:[bold] -> {spec.origin}[/bold]")
    else:
        colored.print("\n... [bold red]source code path not found[/bold red]:")

    if open_url and "Home-page" in metadata:
        colored.print(f"Opening homepage: {metadata['Home-page']}")
        webbrowser.open(metadata["Home-page"])

def preview(slow: tuple[bool, int] = (False, 1), preview_rate=3, text_in_preview=""):
    """ Preview fonts with optional slow mode.
        Args: -> slow (tuple): (enabled: bool, delay_seconds: int) """

    slow_enabled, delay = slow
    for idx, name in enumerate(fonts, start=1):
        colored.print(f"\nindex: [bold yellow]{idx:<6}[/bold yellow][bold]font name[/bold]: [bold yellow]->[/bold yellow] [bold green]{name}[/bold green]")
        colored.print("[bold]=[/bold]" * 60)
        if idx % preview_rate == 0:
            lib.setFont(font=name)
            colored.print(lib.renderText(text_in_preview))
            if slow_enabled:
                sleep(delay)

    colored.print(f"\n[bold green]Total fonts:[/bold green] {len(fonts)}")


if __name__ == "__main__":
    # pass
    lib = Figlet()
    fonts = lib.getFonts()
    preview(slow=(True, 1), preview_rate=1, text_in_preview="Hello World")
    
    # preview(preview_rate=1, text_in_preview="Catalog")
    # pkgs = ["rich", "pyfiglet"]
    # inspect_lib(lib_name=pkgs[-1], open_url=True)
    # [print(f"index: {index_count:<10} font name: -> {name:>21}") for index_count, name in enumerate(pkgs[0], start=1)]
    # [print(f"index: {indx:<10} font name: -> {font_name:>21}") for indx, font_name in enumerate(lib.getFonts(), start=1)]
    # [print(line) for lib in pkgs for line in inspect_lib(lib)]