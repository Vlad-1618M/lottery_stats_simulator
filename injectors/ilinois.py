#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
console = Console()


def headers():
    return {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }


def selectors():
    return {
        "powerball": {
            "container": "li[data-test-id^='draw-result-']",
            "date": "span[data-test-id^='draw-result-info-date-']",
            "primary": "div[data-test-id^='ball-primary-']",
            "secondary": "div[data-test-id^='ball-secondary-']",
            "multiplier": "span[data-test-id^='game-multiplier-']",
        },
        "megamillions": {
            "container": "li[data-test-id^='draw-result-']",
            "date": "span[data-test-id^='draw-result-info-date-']",
            "primary": "div[data-test-id^='ball-primary-']",
            "secondary": "div[data-test-id^='ball-secondary-']",
            "multiplier": "span[data-test-id^='game-multiplier-']",
        },
        "lotto": {
            "container": "li[data-test-id^='draw-result-']",
            "date": "span[data-test-id^='draw-result-info-date-']",
            "primary": "div[data-test-id^='ball-primary-']",
            "secondary": None,
            "multiplier": "span[data-test-id^='game-multiplier-']",
        },
        "luckydaylotto": {
            "container": "li[data-test-id^='draw-result-']",
            "date": "span[data-test-id^='draw-result-info-date-']",
            "primary": "div[data-test-id^='ball-primary-']",
            "secondary": None,
            "multiplier": None,
        },
        "pick3": {
            "container": "li[data-test-id^='draw-result-']",
            "date": "span[data-test-id^='draw-result-info-date-']",
            "primary": "div[data-test-id^='ball-primary-']",
            "secondary": None,
            "multiplier": None,
        },
        "pick4": {
            "container": "li[data-test-id^='draw-result-']",
            "date": "span[data-test-id^='draw-result-info-date-']",
            "primary": "div[data-test-id^='ball-primary-']",
            "secondary": None,
            "multiplier": None,
        },
    }


def urls():
    return [
        "https://www.illinoislottery.com/dbg/results/powerball",
        "https://www.illinoislottery.com/dbg/results/megamillions",
        "https://www.illinoislottery.com/dbg/results/lotto",
        "https://www.illinoislottery.com/dbg/results/luckydaylotto",
        "https://www.illinoislottery.com/dbg/results/pick3",
        "https://www.illinoislottery.com/dbg/results/pick4"
    ]


if __name__ == "__main__":
    pass
