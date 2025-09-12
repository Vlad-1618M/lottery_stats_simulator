# test_browser.py
from playwright.sync_api import sync_playwright
import time

def urls():
    return [
        "https://www.illinoislottery.com/dbg/results/powerball",
        "https://www.illinoislottery.com/dbg/results/megamillions",
        "https://www.illinoislottery.com/dbg/results/lotto",
        "https://www.illinoislottery.com/dbg/results/luckydaylotto",
        "https://www.illinoislottery.com/dbg/results/pick3",
        "https://www.illinoislottery.com/dbg/results/pick4"
    ]

with sync_playwright() as p:
    print("Launching browser...")
    browser = p.chromium.launch(
        headless=False,
        channel="chrome",
        slow_mo=1000
    )
    page = browser.new_page()
    print("Navigating to page...")
    page.goto(urls()[0])
    page.goto(urls()[1])
    page.goto(urls()[2])
    page.goto(urls()[3])
    page.goto(urls()[4])
    page.goto(urls()[5])
    # page.goto('https://example.com')

    print("\t --> did Browser come up ?? ")
    time.sleep(10)
    browser.close()
    print("\nBrowser closed:")

# if __name__ == "__main__":
#     print(urls()[1])