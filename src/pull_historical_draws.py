#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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

arrow = "[bold green]→[/bold green]"
check = "[bright_green]✓ [/bright_green]"

class LottoScraper:
    def __init__(self, urls, output_dir="historical_lotto_draw_results", delay=1.5):
        self.urls = urls
        self.delay = delay
        self.visible_mode = False
        self.keep_open = False
        self.request_count = 0
        self.browser_instance = None

        static_workdir = Path(__file__).resolve().parents[1]
        self.output_dir = static_workdir / output_dir
        self.screenshot_dir = static_workdir / "historical_lotto_screenshots"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        console.rule("[bright_green]*** [bold yellow]Init Scraper[/bold yellow] ***[/bright_green]")
        console.print(f"\n[bold green]✓[/bold green] Screenshot directory created: {arrow} [bright_cyan]{os.path.basename(self.screenshot_dir)}[/bright_cyan]")

        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.headers = dict(ilinois.headers())

    def get_browser(self):
        if self.browser_instance is None:
            headless = not self.visible_mode
            p = sync_playwright().start()
            self.browser_instance = p.chromium.launch(
                headless=headless,
                channel="chrome",
                slow_mo=1000 if not headless else 0,
                args=['--disable-blink-features=AutomationControlled']
            )
        return self.browser_instance

    def close_browser(self):
        if self.browser_instance:
            self.browser_instance.close()
            self.browser_instance = None

    def browser_imitator(self, url, screenshot=False, all_screenshots=False, filename=""):
        try:
            if self.request_count > 0:
                time.sleep(1.0)
            self.request_count += 1
            browser = self.get_browser()
            context = browser.new_context(
                user_agent=self.headers["User-Agent"],
                viewport={'width': 1920, 'height': 1080}
            )
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => false });
            """)
            page = context.new_page()
            console.print(f"[ [bold cyan]mapping url[/bold cyan]]:\t{arrow} [bright_cyan_italic]{url}[/bright_cyan_italic]")
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(2000)
            results = self.handle_pagination(page, url, screenshot, all_screenshots, filename)
            context.close()
            return results
        except Exception as playwright_error:
            console.print(f"\n[bright_red]Playwright Error[/bright_red]: {arrow} [bold]{playwright_error}[/bold]")
            return []

    def handle_pagination(self, page, url, screenshot=False, all_screenshots=False, filename=""):
        all_results = []
        max_attempts = 200
        attempts = 0
        game = Path(url).name.lower()
        selectors = ilinois.selectors().get(game)
        
        next_selectors = [
            'button[aria-label*="next"], button[aria-label*="Next"]',
            'a[aria-label*="next"], a[aria-label*="Next"]',
            'button:has-text(">"), a:has-text(">")',
            '.pagination-next, .next-page, .load-more'
        ]
        
        while attempts < max_attempts:
            try:
                html = page.content()
                results = self.extract_results(html, selectors, game)
                all_results.extend(results)
                
                if attempts % 10 == 0:
                    console.print(f"\n\t{check}\t [white_italic]{str(url).split("/")[-1].upper()}[/white_italic]: [bold magenta]Bulk Page[/bold magenta]: {attempts + 1} [bold]content captured[/bold] {arrow} [bold magenta]processing[/bold magenta] ...")
                
                # Capture screenshot for this page
                if (screenshot and attempts == 0) or all_screenshots:
                    screenshot_path = self.screenshot_dir / (f"{filename.replace('.json', '')}_page{attempts + 1}.png" if all_screenshots else filename.replace(".json", ".png"))
                    page.screenshot(path=str(screenshot_path), full_page=True)
                    console.print(f"\t{check}\t [dim]screenshot:[/dim]\t[bold green]Saved[/bold green]: "
                                  f"[dim]file name & count[/dim]:\t{arrow:>2} {attempts + 1:<4} [yellow italic] {os.path.basename(screenshot_path)}[/yellow italic]")
                clicked = False
                for selector_group in next_selectors:
                    try:
                        elements = page.query_selector_all(selector_group)
                        for element in elements:
                            if element.is_visible():
                                disabled = element.get_attribute('disabled') or element.get_attribute('aria-disabled')
                                if not disabled:
                                    element_text = element.text_content().strip() or element.get_attribute('aria-label') or "pagination element"
                                    console.print(f"\t{arrow}\t [dim]page element:[/dim]\t[bold yellow]click[/bold yellow]: "
                                                  f"[bright_cyan]{element_text.upper()}[/bright_cyan] [dim]page count[/dim]:\t{arrow:>2} [bold magenta]{attempts + 1:<4}[/bold magenta]")
                                    element.click()
                                    page.wait_for_timeout(1500)
                                    page.wait_for_load_state('domcontentloaded', timeout=8000)
                                    clicked = True
                                    break
                        if clicked:
                            break
                    except:
                        continue
                
                if not clicked:
                    console.rule("[bright_green]*** [bold yellow]DONE Init Scraper Completed[/bold yellow] ***[/bright_green]")
                    console.print(f"\n[bold yellow]clicked through all available page elements[/bold yellow]: "
                                  f"Element Name: {arrow} [bright_cyan]{element_text.upper()}[/bright_cyan] "
                                  f"Click Count: {arrow} [bold magenta]{attempts}[/bold magenta]")
                    break
                
                attempts += 1
                
            except Exception as element_error:
                console.print(f"\t[bright_yellow]Pagination[/bright_yellow]: [bold red]issue[/bold red]: {arrow} [bold]{element_error}[/bold]")
                break

        console.print(f"\n[bright_green]Page Paginations Completed[/bright_green]: {arrow} [bold yellow]Total Pages[/bold yellow]: [bold magenta] {attempts} [/bold magenta]")
        return all_results

    def get_page_content(self, url, screenshot=False, all_screenshots=False, filename=""):
        try:
            if self.request_count > 0:
                time.sleep(self.delay)
            self.request_count += 1
            resp = self.session.get(url, headers=self.headers, timeout=8, verify=False)
            resp.raise_for_status()
            game = Path(url).name.lower()
            selectors = ilinois.selectors().get(game)
            results = self.extract_results(resp.text, selectors, game)
            if screenshot or all_screenshots:
                self.browser_imitator(url, screenshot, all_screenshots, filename)
            return results
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response.status_code == 403:
                return self.browser_imitator(url, screenshot, all_screenshots, filename)
            return []
        except Exception:
            return self.browser_imitator(url, screenshot, all_screenshots, filename)

    def extract_results(self, html, selectors, game):
        soup = BeautifulSoup(html, "html.parser")
        results = []
        secondary_ball_name = "mega" if "megamillions" in game else "powerball"
        container_selector = selectors.get("container")
        if not container_selector:
            return results
        draw_items = soup.select(container_selector)
        for item in draw_items:
            result = {
                "draw_date": self.get_text(item, selectors.get("date")),
                "primary_numbers": [b.get_text(strip=True) for b in item.select(selectors["primary"])] if selectors.get("primary") else [],
                secondary_ball_name: self.get_text(item, selectors.get("secondary")),
                "multiplier": self.get_text(item, selectors.get("multiplier")),
            }
            results.append(result)
        return results

    def get_text(self, element, selector):
        if not selector:
            return "N/A"
        found = element.select_one(selector)
        return found.get_text(strip=True) if found else "N/A"

    def generate_filename(self, url):
        slug = urlparse(url).path.rstrip("/").split("/")[-1] or "index"
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", slug)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        url_hash = hashlib.sha1(url.encode()).hexdigest()[:4]
        return f"{safe}_{timestamp}_{url_hash}.json"

    def process_url(self, url, screenshot=False, all_screenshots=False):
        console.print(f"[ [bold yellow]args check[/bold yellow] ]:\t{arrow} [bold white]Screenshot[/bold white]=[bold]{screenshot}[/bold]: [bold white]All Screenshots[/bold white]=[bold]{all_screenshots}[/bold]")
        start_time = time.time()
        filename = self.generate_filename(url)
        results = self.get_page_content(url, screenshot, all_screenshots, filename)
        if not results:
            console.print("[bright_red]\tFailed[/bright_red]: to fetch content:\n")
            return False
        game = Path(url).name.lower()
        selectors = ilinois.selectors().get(game)
        if not selectors:
            console.print(f"\n\t[/bright_red]No Selectors[/bright_red]: found for: {arrow} [bold_yellow]{game}[/bold_yellow]\n" + "[dim]-[dim]" * 50)
            return False
        if not results:
            console.print("\n[bold red]No Results found[/bold red]\n" + "[dim]-[dim]" * 50)
            return True
        secondary_ball_name = "mega" if "megamillions" in game else "powerball"
        original_format_results = []
        for result in results:
            original_result = {
                "draw_date": result["draw_date"],
                "primary_numbers": [", ".join(result["primary_numbers"])],
                secondary_ball_name: result[secondary_ball_name],
                "multiplier": result["multiplier"]
            }
            original_format_results.append(original_result)
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(original_format_results, f, indent=4)
        elapsed = time.time() - start_time
        console.print(f"Overall count of [bold]{len(results)}[/bold] results in [bold blue]{elapsed:.1f}s[/bold blue] {arrow} file name: [white]{filepath.name}[/white]")
        return True

    def run(self, screenshot=False, all_screenshots=False, visible_mode=False, keep_open=False):
        self.visible_mode = visible_mode
        self.keep_open = keep_open
        console.print(f"\t[bright_cyan]Sequentiall Processing[/bright_cyan]: total url count: {arrow} [bold magenta]{len(self.urls)}[/bold magenta]")
        console.print(f"\t[dim]Current Delay[/dim]: \t\t{arrow} [bold magenta]{self.delay}s[/bold magenta]:"
                      f"\n\t[dim]Screenshots[/dim]: \t\t{arrow} [bold magenta]{screenshot}[/bold magenta]"
                      f"\n\t[dim]All Screenshots[/dim]:\t{arrow} [bold magenta]{all_screenshots}[/bold magenta]\n")
        
        successful = 0
        total_start = time.time()
        for idx, url in enumerate(self.urls, 1):
            console.print(f"[ [bold magenta]processing[/bold magenta] ]:\t{arrow} "
                          f"[bright_cyan]{idx}[/bright_cyan] out of [bold yellow]{len(self.urls)}[/bold yellow] [bold magenta]main urls[/bold magenta]:")
            
            success = self.process_url(url, screenshot, all_screenshots)
            if success:
                successful += 1
            if idx < len(self.urls):
                elapsed = time.time() - total_start
                estimated_total = (elapsed / idx) * len(self.urls)
                remaining = estimated_total - elapsed
                console.print(f"[bold magenta]Progress:[/bold magenta] {arrow} "
                              f"[bright_cyan]{idx}[/bright_cyan][bold]/[/bold][bold yellow]{len(self.urls)}[/bold yellow] {arrow} "
                              f"[bold magenta]Elapsed[/bold magenta]: [bold]{elapsed:.0f}[/bold]s {arrow} "
                              f"[bright_yellow]ETA[/bright_yellow]: [bold magenta]{remaining:.0f}[/bold magenta]s\n")
                time.sleep(self.delay)
        total_time = time.time() - total_start
        console.print(f"\n[green]✓ Completed {successful}/{len(self.urls)} URLs in {total_time:.0f}s[/green]")
        if not self.keep_open:
            self.close_browser()


def main():
    get_screenshots = "--shots" in sys.argv
    all_screenshots = "--all-shots" in sys.argv
    visible_mode = "--visible" in sys.argv or "--headless=false" in sys.argv
    keep_open = "--keep-open" in sys.argv
    base_delay = 1.0
    scraper = LottoScraper(ilinois.urls(), delay=base_delay)
    scraper.run(
        screenshot=get_screenshots, 
        all_screenshots=all_screenshots,
        visible_mode=visible_mode,
        keep_open=keep_open
    )


if __name__ == "__main__":
    main()