#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import json
import time
import urllib3
import hashlib
import requests
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from rich.console import Console
from urllib.parse import urlparse
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).resolve().parents[1]))
from logger import logger_main
from injectors import ilinois

console = Console()
log_it = logger_main.get_logger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LottoScraper:
    def __init__(self, urls, output_dir="lotto_draw_results", delay=0.0):
        self.urls = urls
        self.delay = delay

        static_workdir = Path(__file__).resolve().parents[1]
        self.output_dir = static_workdir / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()

        retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.headers = dict(ilinois.headers())

    def browser_imitator(self, url):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(user_agent=self.headers["User-Agent"])
                page = context.new_page()
                console.print(f"[yellow]→ maping url:[/yellow] [cyan]{url}[/cyan]")
                # page.goto(url, wait_until="networkidle", timeout=30000)
                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(5000)
                content = page.content()
                browser.close()
                return content
        except Exception as playwright_error:
            console.log(f"Playwright error for {url}: {playwright_error}")
            log_it.error(f"{url} error: {playwright_error}")
            return None

    def get_page_content(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=10, verify=False)
            resp.raise_for_status()
            if "text/html" not in resp.headers.get("Content-Type", ""):
                return None
            return resp.text
        except requests.exceptions.HTTPError as call_error:
            log_it.warning({call_error})
            if resp.status_code == 403:
                return self.browser_imitator(url)
            return None
        except Exception:
            return self.browser_imitator(url)

    def extract_results(self, html, selectors):
        soup = BeautifulSoup(html, "html.parser")
        results = []

        draw_items = soup.select(selectors["container"])
        for item in draw_items:
            date_element = item.select_one(selectors["date"]) if selectors["date"] else None
            primary_balls = item.select(selectors["primary"]) if selectors["primary"] else []
            secondary_ball = item.select_one(selectors["secondary"]) if selectors["secondary"] else None
            multiplier_element = item.select_one(selectors["multiplier"]) if selectors["multiplier"] else None

            results.append({
                "draw_date": date_element.get_text(strip=True) if date_element else "N/A",
                "primary_numbers": [b.get_text(strip=True) for b in primary_balls],
                "powerball": secondary_ball.get_text(strip=True) if secondary_ball else "N/A",
                "multiplier": multiplier_element.get_text(strip=True) if multiplier_element else "N/A",
            })

        return results

    def generate_filename(self, url):
        parts = urlparse(url)
        slug = parts.path.rstrip("/").split("/")[-1] or "index"
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", slug)
        token = hashlib.sha1(url.encode()).hexdigest()[:6]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{safe}_{timestamp}_{token}.json"

    def get_lotto_screenshot(self, url, filename):
        try:
            screenshot_dir = self.output_dir.parent / "lotto_screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / filename.replace(".json", ".png")

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(user_agent=self.headers["User-Agent"])
                page = context.new_page()
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(3000)
                page.screenshot(path=str(screenshot_path), full_page=True)
                browser.close()

            console.print(f"[green]✔ Screenshots:[/green] [bold]{screenshot_path}[/bold]")
        except Exception as e:
            console.print(f"[red]Failed to capture screenshot:[/red] {e}")
            log_it.error(f"{url} screenshot failed: {e}")

    def process_url(self, url, screenshot=False):
        console.print(f"\n[yellow]→[/yellow] [magenta]Processing:[/magenta] [white dim]{url}[/white dim]")
        html = self.get_page_content(url)
        if not html:
            console.print(f"[red]Failed to fetch content from {url}[/red]")
            return

        game = Path(url).name.lower()
        selectors = ilinois.selectors().get(game)

        if not selectors:
            console.print(f"\n[red]No selector mapping found for:[/red] [magenta]{game}[/magenta]")
            return

        results = self.extract_results(html, selectors)
        if not results:
            console.print(f"[red]No results found at {url}[/red]")
            snippet = html[:400].replace("\n", " ").strip()
            console.print(f"\n[dim]HTML snippet:[/dim] {snippet}")
            return

        filename = self.generate_filename(url)
        filepath = self.output_dir / filename
        raw_json = json.dumps(results, indent=4)
        compacted = re.sub(r'"primary_numbers": \[\s+(.*?)\s+\]', lambda m: '"primary_numbers": [' + ' '.join(x.strip() for x in m.group(1).splitlines()) + ']', raw_json, flags=re.DOTALL)

        with open(filepath, "w", encoding="utf-8") as artifact:
            artifact.write(compacted)

        console.print(f"[green]✔ Artifact:[/green] [bold]{filepath}[/bold]")

        if screenshot:
            self.get_lotto_screenshot(url, filename)

        console.print("[white]-[/white]" * len(url))

        if self.delay > 0:
            time.sleep(self.delay)

    def run(self, screenshot=False):
        for url in self.urls:
            self.process_url(url, screenshot=screenshot)


def main():
    get_screenshots = "--shots" in sys.argv
    scraper = LottoScraper(ilinois.urls())
    scraper.run(screenshot=get_screenshots)


if __name__ == "__main__":
    main()
