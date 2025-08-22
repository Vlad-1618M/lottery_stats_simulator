# Get Lotto Results:
[get_lotto_results.py](/src/get_lotto_results.py) script scrapes latest lottery draw results from specified [urls](/injectors/ilinois.py): <br>
Pulls data using [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) and saves results in parsed `.json` files: <br>
Supports screenshot capture with `https` retries where fallback to [Playwright](https://playwright.dev/python/docs/intro) for dynamic content is considered:

### Features:
- Scrapes lottery results from configured [urls](/injectors/ilinois.py):
>- game date: 
>- primary number sequence in play (`e.g.`, `> 1` first number selection sets:)  
>- powerball multiplier: (`e.g.`, `powerball`, `mega` as last sinlge number selection sets:)
>- Saves results as JSON in `lotto_draw_results/` dir:
>- Optionally captures screenshots of source pages if `--shots` flag was used:
>- Handles `https` errors with retries and [Playwright](https://playwright.dev/python/docs/intro) for `JavaScript` rendered pages:

### Dependencies:
- Python 3.11
>- [requests](https://pypi.org/project/requests/) 
>- [urllib3](https://pypi.org/project/urllib3/)
>- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
>- [Playwright](https://playwright.dev/python/docs/intro)
- see [requirements.txt](/deps/requirements.txt) for version details:
- [logger_main.py](/logger/logger_main.py)
- [ilinois.py](/injectors/ilinois.py)

### CLI Examples & Command Description:
- Scrape results parsed in `.josn`:
```bash
python3 src/get_lotto_results.py

→ Processing: https://www.illinoislottery.com/dbg/results/powerball

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:36:57,507
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/powerball')}
→ maping url: https://www.illinoislottery.com/dbg/results/powerball
✔ Artifact: /lotto_simulator/lotto_draw_results/powerball_2025-08-14_13-37-11_abea1f.json
-----------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/megamillions

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:37:11,569
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/megamillions')}
→ maping url: https://www.illinoislottery.com/dbg/results/megamillions
✔ Artifact: /lotto_simulator/lotto_draw_results/megamillions_2025-08-14_13-37-18_ff2c6d.json
--------------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/lotto

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:37:19,143
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/lotto')}
→ maping url: https://www.illinoislottery.com/dbg/results/lotto
✔ Artifact: /lotto_simulator/lotto_draw_results/lotto_2025-08-14_13-37-26_53f166.json
-------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/luckydaylotto

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:37:26,773
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/luckydaylotto')}
→ maping url: https://www.illinoislottery.com/dbg/results/luckydaylotto
✔ Artifact: /lotto_simulator/lotto_draw_results/luckydaylotto_2025-08-14_13-37-34_4889a8.json
---------------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/pick3

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:37:34,428
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/pick3')}
→ maping url: https://www.illinoislottery.com/dbg/results/pick3
✔ Artifact: /lotto_simulator/lotto_draw_results/pick3_2025-08-14_13-37-41_1c1f11.json
-------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/pick4

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:37:41,919
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/pick4')}
→ maping url: https://www.illinoislottery.com/dbg/results/pick4
✔ Artifact: /lotto_simulator/lotto_draw_results/pick4_2025-08-14_13-37-49_4a6ed4.json
```
```bash
    tree lotto_draw_results
    lotto_draw_results
    ├── lotto_2025-08-14_13-37-26_53f166.json
    ├── luckydaylotto_2025-08-14_13-37-34_4889a8.json
    ├── megamillions_2025-08-14_13-37-18_ff2c6d.json
    ├── pick3_2025-08-14_13-37-41_1c1f11.json
    ├── pick4_2025-08-14_13-37-49_4a6ed4.json
    └── powerball_2025-08-14_13-37-11_abea1f.json

    1 directory, 6 files
```
![draw results json](/docs/lotto_draw_results_json_example.png)

- Scrape results aparsed in `.josn` plus capture screenshots: 
- `--shots`

```bash
 python3 src/get_lotto_results.py --shots

→ Processing: https://www.illinoislottery.com/dbg/results/powerball

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:43:59,406
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/powerball')}
→ maping url: https://www.illinoislottery.com/dbg/results/powerball
✔ Artifact: lotto_simulator/lotto_draw_results/powerball_2025-08-14_13-44-10_abea1f.json
✔ Screenshots: lotto_simulator/lotto_screenshots/powerball_2025-08-14_13-44-10_abea1f.png
-----------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/megamillions

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:44:16,711
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/megamillions')}
→ maping url: https://www.illinoislottery.com/dbg/results/megamillions
✔ Artifact: lotto_simulator/lotto_draw_results/megamillions_2025-08-14_13-44-24_ff2c6d.json
✔ Screenshots: lotto_simulator/lotto_screenshots/megamillions_2025-08-14_13-44-24_ff2c6d.png
--------------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/lotto

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:44:30,262
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/lotto')}
→ maping url: https://www.illinoislottery.com/dbg/results/lotto
✔ Artifact: lotto_simulator/lotto_draw_results/lotto_2025-08-14_13-44-37_53f166.json
✔ Screenshots: lotto_simulator/lotto_screenshots/lotto_2025-08-14_13-44-37_53f166.png
-------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/luckydaylotto

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:44:43,999
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/luckydaylotto')}
→ maping url: https://www.illinoislottery.com/dbg/results/luckydaylotto
✔ Artifact: lotto_simulator/lotto_draw_results/luckydaylotto_2025-08-14_13-44-51_4889a8.json
✔ Screenshots: lotto_simulator/lotto_screenshots/luckydaylotto_2025-08-14_13-44-51_4889a8.png
---------------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/pick3

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:44:57,286
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/pick3')}
→ maping url: https://www.illinoislottery.com/dbg/results/pick3
✔ Artifact: lotto_simulator/lotto_draw_results/pick3_2025-08-14_13-45-04_1c1f11.json
✔ Screenshots: lotto_simulator/lotto_screenshots/pick3_2025-08-14_13-45-04_1c1f11.png
-------------------------------------------------

→ Processing: https://www.illinoislottery.com/dbg/results/pick4

	LOG-LEVEL:	 -> WARNING:
	Time-Date:	 -> 2025-08-14 13:45:10,838
	MODULE-SRC:	 -> get_lotto_results: -> Line # 71
	MESSAGE:	 -> {HTTPError('403 Client Error: Forbidden for url: https://www.illinoislottery.com/dbg/results/pick4')}
→ maping url: https://www.illinoislottery.com/dbg/results/pick4
✔ Artifact: lotto_simulator/lotto_draw_results/pick4_2025-08-14_13-45-18_4a6ed4.json
✔ Screenshots: lotto_simulator/lotto_screenshots/pick4_2025-08-14_13-45-18_4a6ed4.png
-------------------------------------------------
```
![megamillion](/docs/lotto_screenshots_examples/megamillions_2025-08-14_13-44-24_ff2c6d.png)
---
![powerball](/docs/lotto_screenshots_examples/powerball_2025-08-14_13-44-10_abea1f.png)
---
![lotto](/docs/lotto_screenshots_examples/lotto_2025-08-14_13-44-37_53f166.png)
----------------------------------------

#### Functions Description:
- `class LottoScraper: `
- Scraper init:
```python
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
```
- `browser_imitator(self, url):`
- Page content fetche | plugin Playwright for dynamic sites:
```python
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
```

- `get_page_content(self, url):`
- `html` retries | goes back to `Playwright` if call is stubborn on errors:
```python
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
```
- `extract_results(self, html, selectors):`
- BeautifulSoup to get draw results + game specific selectors:
```python
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
```

- `generate_filename(self, url):`
- write unique json file names with url slug and timestamp to avide naming conflicst on rerans:
```python
    def generate_filename(self, url):
        parts = urlparse(url)
        slug = parts.path.rstrip("/").split("/")[-1] or "index"
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", slug)
        token = hashlib.sha1(url.encode()).hexdigest()[:6]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{safe}_{timestamp}_{token}.json"
```

- `get_lotto_screenshot(self, url, filename):`
- Playwright captures page screenshot:
```python
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
```

- `process_url(self, url, screenshot=False):`
- urls processor:
- kepp results + optional screenshot:
```python
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
```

- `run(self, screenshot=False):`
- Run them all: helper functon:
```python
    def run(self, screenshot=False):
        for url in self.urls:
            self.process_url(url, screenshot=screenshot)
```
- `main()`
- Initialize class `LottoScraper(ilinois.urls())` scraper:
- Run main logic + optional screenshot if true:
```python
def main():
    get_screenshots = "--shots" in sys.argv
    scraper = LottoScraper(ilinois.urls())
    scraper.run(screenshot=get_screenshots)


if __name__ == "__main__":
    main()
```
---
### Notes:
- `urls` and selectors are defined in [ilinois.py](/injectors/ilinois.py) config:
- `.json` data results kept in `/lotto_draw_results/` dynamic, therefore ignored -- see `.gitignore` config:
- `.png` screenshots kept in `/lotto_screenshots/` dynamic, therefore ignored  -- see `.gitignore` config:
```bash
    # local:
    .logs
    lotto_draw_results
    lotto_screenshots
    lottery_catalog
    /build/gotools/go_compiled
    html_reports
    Aug-*
    June-*
    July-*
    August-*
```
- [Playwright](https://playwright.dev/python/docs/intro) requires installation: (`playwright install`) for screenshot and fallback to scraping logic: 
- This is also handled in --> [_setup.Dockerfile](/build/amd/amd_setup.Dockerfile): 
```bash
RUN playwright install-deps && \
    playwright install 
```
- all errors `logs` go to logger_main.get_logger(__name__)
- logger records are dynamic, therefore ignored  -- see `.gitignore` config:

>- .logs file examplke:
![.logs](/docs/logs_file_example.png)

### License:
- See LICENSE in the repository root for licensing details:
----
