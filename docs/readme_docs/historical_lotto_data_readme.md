# [Historical Lotto Data Scraper](/src/pull_historical_draws.py)
## Is a Python-based web scraper designed to collect comprehensive historical lottery draw results for data analysis and pattern recognitions:

## Purpose:
The need for complete historical lottery data cameup as a critical gap in pipeline data analytics:
This tool was developed to fill that gap:
> The collected data enables:
>  - Game play sequence analysis for predictive modeling:
>  - Pattern recognition of number frequency and distributions:
>  - Statistical analysis of rare vs common number sequences:
>  - Helps in ML training datasets for prediction algorithms:
>  - Strategic game play suggestions based on historical trends:

## Architectural Decisions:
* ***__Sequential Processing__*** over ***_Parallel Execution_*** and why ***_Sequential_*** was chosen:<br>
> - Anti-Bot Protection: - Lottery websites often employ ***anti-scraping*** measures:
>   - Rate limiting + request throttling:
>   - IP blocking for concurrent requests:
>   - JavaScript challenges and CAPTCHAs:
---
> - Resource Management: - ***Playwright*** instances are resource-intensive:
>   - Each browser instance consumes significant RAM (200-500MB each):
>   - Multiple instances exhaust sys resources much quicker than results are stacked up in buffer:
>   - Network pipe saturation from concurrent connections:
---
> - Reliability over Speed: - data integrity is > important: 
>   - Sequential processing ensures complete page pagination:
>   - Reduces risk of missed data due to race conditions:
>   - Better error handling and recovery:
---
>   - Stealth Requirements: -  e.g (***mimicking human behavior patterns***)
>      - Natural timing between requests helps to avoid detection:
>      - Sequential navigation through pagination appears organic:
>      - Helps to reduce a fingerprinting risk:
---

### Comparison with ***__Alternative Approaches__***:<br>
 > - _***ThreadPool***_:
 >   - ***___Pros:___*** - Fast processing:
 >   - ***___Cons:___***
 >      - Triggers anti-bot protection:
 >      - Resource exhaustion:
 > - ***__Why Not Chosen:__***
 >    - Unreliable pagination:
 >    - High failure rate on protected sites:
----
 > - _***AsyncI0:***_
 >   - ***___Pros:___*** - Efficient I/O handling:
 >   - ***___Cons:___***
 >      - Complex error handling:
 >      - Playwrights async complexity:
 > - ***__Why Not Chosen:__***
 >      - More complexity VS reliability benefits:
----
 > - _***Multiprocessing:***_
 >   - ***___Pros:___*** - Ok Parallelism:
 >   - ***___Cons:___***
 >      - High memory usage:
 >      - Process synchronization issues:
 > - ***__Why Not Chosen:__***
 >      - Resource prohibitive for scaled scraping:
----

### Tech-Stack Analysis:
> - _***BeautifulSoup4 (BS4):***_
---
 >   - ***___Pros:___*** 
 >      - Lightweight / fast HTML parsing:
 >      - Simple CSS selector syntax:
 >      - Low memory footprint:
 >      - Excellent for static content extraction:
 >   - ***___Cons:___***
 >      - No JavaScript execution capability:
 >      - Unable to handle dynamic content:
 >      - Limited to already-loaded HTML:
 >   - ***___Use Case:___***
 >      - Primary content extraction from already-rendered pages:
---
 > - _***Playwright:***_
---
 >   - ***___Pros:___*** 
 >      - Full browser automation with JavaScript execution:
 >      - Handles dynamic content and SPAs (___Single Page Applications___):
 >      - Built-in waiting mechanisms and auto-retry:
 >      - Cross-browser support:
 >   - ***___Cons:___***
 >      - Resource-intensive (memory/CPU):
 >      - Slower than HTTP requests:
 >      - Complex setup and maintenance:
 >   - ***___Use Case:___***
 >      - JavaScript rendering: 
 >      - Pagination handling:
 >      - Screenshot capture:
 ---
 > - _***Hybrid Approach Benefits:***_
  >   - BS4 + Playwright combination gets:
  >      - Efficiency: - BS4 for fast parsing of static content:
  >      - Capability: - Playwright for JavaScript-dependent functionality:
  >      - Reliability: - Fallback mechanisms between techniques:
  >      - Flexibility: - Adaptable to different website structures:
---
 > - _***Resulted Features in Code:***_
  >      - Good Pagination Handling:
  >      - Automatic detection and clicking of "Next" buttons:
  >      - Comprehensive selector strategies for different pagination patterns:
  >      - Resume capabilities + progress tracking: 
  >      - Dual data extraction:
  >         - Primary: - Fast BS4 parsing for efficient data extraction:
  >         - Secondery: - Playwright rendering for JavaScript-heavy sites:
  >      - Hybrid: 
  >         - Optimal combination based on content type:
  >         - Comprehensive Data Capture:
  >         - Complete historical draw results:
  >         - Multiple lottery game types support:
  >         - Structured .json + consistent formatting output:
  >         - Optional screenshot documentation:
  >         - Stealth + Reliability:
  >         - Randomized delays between requests:
  >         - Browser fingerprint mitigation:
  >         - Automatic retry mechanisms
  >         - Error recovery and continuation:
  >         - Data Output Format:
  ---
```json
              [
                {
                  "draw_date": "Sep 9, 2025",
                  "primary_numbers": ["3, 16, 29, 61, 69"],
                  "powerball": "22",
                  "multiplier": "N/A"
                }
              ]
```
---
> - _***Supported Lottery Games:***_:
>   - Powerball:
>   - Mega Millions:
>   - Lotto:
>   - Lucky Day Lotto:
>   - Pick 3:
>   - Pick 4:

---
### Call Examples:
  ```bash
  python src/historical_lotto_scraper.py                      # basic data collection:
  python src/historical_lotto_scraper.py --shots              # with screenshots:
  python src/historical_lotto_scraper.py --shots --all-shots  # all or every page screenshots:
  python src/historical_lotto_scraper.py --visible            # visible browser mode [debugging]:
  ```
---
> - _***Configuration:***_
>   - Delay Control: - Adjust request timing between URLs:
>   - Output Directories: - Separate data and screenshot locations:
>   - Retry Settings: - Configurable retry attempts and backoff:
>   - Browser Options: - Headless/headed mode selection:
---
> - _***Anti-Detection Measures:***_
>   - Realistic browser fingerprints:
>   - Randomized user-agent patterns:
>   - Natural mouse movement simulation:
>   - Request timing variability:
>   - DOM environment masking:
---
> - _***Performance Considerations:***_
>   - Memory: ~300MB per Playwright instance:
>   - Network: Sequential requests to avoid saturation:
>   - Storage: JSON data + optional PNG screenshots:
>   - Time: ~2-3 seconds per page (varies by site complexity):
---

# License & Usage:
* This tool is designed for educational and research purposes: <br>
  - Users should:
    - Respect website terms of service:
    - Implement rate limiting appropriately:
    - Use data responsibly and ethically:
    - Consider legal implications in their jurisdiction:

- Built for reliable historical data collection where completeness and accuracy matter more than speed:
___

