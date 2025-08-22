# #!/usr/bin/env python
# # -*- config: utf-8 -*-

import sys
import webbrowser
from pathlib import Path
from datetime import datetime
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[1]))
from logger import logger_main

c = Console()
log_it = logger_main.get_logger(__name__)


def save_html_report(func, *args, open_browser: bool = False, output_dir: str = "html_reports", inline_styles: bool = True, **kwargs,):
    """(*args, **kwargs) helps capturing all rich lib output to HTML from everywehre it is called:"""

    html_dir = Path(output_dir)
    html_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    html_path = html_dir / f"sequence_stats_{now}.html"

    base_dir = Path(__file__).resolve().parent
    css_path = base_dir / "theme.css"
    html_console = Console(record=True, width=139)

    # ____ inject console and full-html flag | if not already passed in:
    kwargs.setdefault("console", html_console)
    kwargs.setdefault("save_all_to_html", True)

    # ____ call the actual job:
    func(*args, **kwargs)

    # ____  optionas to export/ inject css:
    html_output = html_console.export_html(inline_styles=inline_styles)

    if css_path.exists():
        marker = "</head>"
        css_raw = css_path.read_text(encoding="utf-8")
        if marker in html_output:
            html_output = html_output.replace(marker, f"<style>\n{css_raw}\n</style>\n{marker}")
        else:
            log_it.warning("Missing </head> marker; prepending CSS.")
            html_output = f"<style>\n{css_raw}\n</style>\n{html_output}"
    else:
        log_it.warning(f"CSS file {css_path.name} not found; continuing without styling.")

    # ___ optional body hook:
    html_output = html_output.replace("<body>", '<body class="dark-report">')
    html_path.write_text(html_output, encoding="utf-8")
    c.print(f"[dim]INFO[/dim] HTML report saved to: [bright_yellow]{html_path.name}[/bright_yellow]")

    if open_browser:
        webbrowser.open(f"file://{html_path.resolve()}")

    return html_path
