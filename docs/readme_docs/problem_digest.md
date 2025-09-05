# Problem Restatement:
### We've got a ton of `.json` files or high count of merged arrays where each record has the following structure:
```json
[
    {
        "timestamp": "2025-08-26T14:18:09.901640",
        "game": "megamillion",
        "selection": {
            "primary": [32,66,36,60,63],
            "primes_in_primary": [],
            "mega": [8],
            "primes_in_mega": []
        }
    },
    {
        "timestamp": "2025-08-26T14:18:09.903182",
        "game": "powerball",
        "selection": {
            "primary": [6,42,45,52,56],
            "primes_in_primary": [],
            "power": [20],
            "primes_in_power": []
        }
    },
    {
        "timestamp": "2025-08-26T14:18:09.905441",
        "game": "lotto",
        "selection": {
            "primary": [32,1,10,46,29,30],
            "primes_in_primary": [29]
        }
    },
    {
        "timestamp": "2025-08-26T14:18:09.907660",
        "game": "luckyday",
        "selection": {
            "primary": [6,43,16,17,30],
            "primes_in_primary": [43,17]
        }
    },
    {
        "timestamp": "2025-08-26T14:18:09.910026",
        "game": "pick3",
        "selection": {
            "primary": [8,9,4],
            "primes_in_primary": []
        }
    },
    {
        "timestamp": "2025-08-26T14:18:09.911530",
        "game": "pick4",
        "selection": {
            "primary": [8,4,5,6],
            "primes_in_primary": [5]
        }
    },
    {
        "timestamp": "2025-08-26T14:19:11.093205",
        "game": "megamillion",
        "selection": {
            "primary": [66,51,21,61,30],
            "primes_in_primary": [61],
            "mega": [13],
            "primes_in_mega": [13]
        }
    },
    {
        "timestamp": "2025-08-26T14:19:11.097000",
        "game": "powerball",
        "selection": {
            "primary": [64,39,11,56,61],
            "primes_in_primary": [11,61],
            "power": [23],
            "primes_in_power": [23]
        }
    },
    {
        "timestamp": "2025-08-26T14:19:11.101292",
        "game": "lotto",
        "selection": {
            "primary": [32,11,43,16,22,29],
            "primes_in_primary": [11,43,29]
        }
    },
    {
        "timestamp": "2025-08-26T14:19:11.105143",
        "game": "luckyday",
        "selection": {
            "primary": [33,4,40,41,31],
            "primes_in_primary": [41,31]
        }
    },
    {
        "timestamp": "2025-08-26T14:19:11.115057",
        "game": "pick3",
        "selection": {
            "primary": [1,2,3],
            "primes_in_primary": [2,3]
        }
    },
    {
        "timestamp": "2025-08-26T14:19:11.117384",
        "game": "pick4",
        "selection": {
            "primary": [0,8,2,4],
            "primes_in_primary": [2]
        }
    },
    {
        "timestamp": "2025-08-26T14:38:29.410587",
        "game": "megamillion",
        "selection": {
            "primary": [10,18,19,24,58],
            "primes_in_primary": [19],
            "mega": [22],
            "primes_in_mega": []
        }
    },
    {
        "timestamp": "2025-08-26T14:38:29.413082",
        "game": "powerball",
        "selection": {
            "primary": [3,41,46,55,31],
            "primes_in_primary": [3,41,31],
            "power": [10],
            "primes_in_power": []
        }
    },
    {
        "timestamp": "2025-08-26T14:38:29.416723",
        "game": "lotto",
        "selection": {
            "primary": [3,39,14,15,23,28],
            "primes_in_primary": [3,23]
        }
    },
    {
        "timestamp": "2025-08-26T14:38:29.419991",
        "game": "luckyday",
        "selection": {
            "primary": [1,2,43,21,31],
            "primes_in_primary": [2,43,31]
        }
    },
    {
        "timestamp": "2025-08-26T14:38:29.423865",
        "game": "pick3",
        "selection": {
            "primary": [9,3,7],
            "primes_in_primary": [3,7]
        }
    },
    {
        "timestamp": "2025-08-26T14:38:29.426611",
        "game": "pick4",
        "selection": {
            "primary": [8,9,5,7],
            "primes_in_primary": [5,7]
        }
    },
    {
        "timestamp": "2025-08-26T14:39:45.902598",
        "game": "megamillion",
        "selection": {
            "primary": [3,69,10,53,25],
            "primes_in_primary": [3,53],
            "mega": [13],
            "primes_in_mega": [13]
        }
    },
    {
        "timestamp": "2025-08-26T14:39:45.906241",
        "game": "powerball",
        "selection": {
            "primary": [38,51,23,56,62],
            "primes_in_primary": [23],
            "power": [20],
            "primes_in_power": []
        }
    },
    {
        "timestamp": "2025-08-26T14:39:45.910250",
        "game": "lotto",
        "selection": {
            "primary": [38,9,42,12,16,30],
            "primes_in_primary": []
        }
    },
    {
        "timestamp": "2025-08-26T14:39:45.913054",
        "game": "luckyday",
        "selection": {
            "primary": [35,7,25,26,31],
            "primes_in_primary": [7,31]
        }
    },
    {
        "timestamp": "2025-08-26T14:39:45.916032",
        "game": "pick3",
        "selection": {
            "primary": [2,3,5],
            "primes_in_primary": [2,3,5]
        }
    },
    {
        "timestamp": "2025-08-26T14:39:45.922202",
        "game": "pick4",
        "selection": {
            "primary": [8,1,2,6],
            "primes_in_primary": [2]
        }
    },
    {
        "timestamp": "2025-08-26T14:41:01.237602",
        "game": "megamillion",
        "selection": {
            "primary": [68,6,16,21,31],
            "primes_in_primary": [31],
            "mega": [1],
            "primes_in_mega": []
        }
    },
    {
        "timestamp": "2025-08-26T14:41:01.241107",
        "game": "powerball",
        "selection": {
            "primary": [39,44,23,58,31],
            "primes_in_primary": [23,31],
            "power": [2],
            "primes_in_power": [2]
        }
    },
    {
        "timestamp": "2025-08-26T14:41:01.245754",
        "game": "lotto",
        "selection": {
            "primary": [3,6,39,43,44,22],
            "primes_in_primary": [3,43]
        }
    },
    {
        "timestamp": "2025-08-26T14:41:01.253656",
        "game": "luckyday",
        "selection": {
            "primary": [35,36,8,44,45],
            "primes_in_primary": []
        }
    },
    {
        "timestamp": "2025-08-26T14:41:01.257383",
        "game": "pick3",
        "selection": {
            "primary": [0,4,5],
            "primes_in_primary": [5]
        }
    },
    {
        "timestamp": "2025-08-26T14:41:01.260498",
        "game": "pick4",
        "selection": {
            "primary": [1,3,4,7],
            "primes_in_primary": [3,7]
        }
    },
    {
        "timestamp": "2025-08-26T14:43:23.749932",
        "game": "megamillion",
        "selection": {
            "primary": [68,12,14,19,24],
            "primes_in_primary": [19],
            "mega": [16],
            "primes_in_mega": []
        }
    },
    {
        "timestamp": "2025-08-26T14:43:23.754075",
        "game": "powerball",
        "selection": {
            "primary": [38,20,23,57,62],
            "primes_in_primary": [23],
            "power": [10],
            "primes_in_power": []
        }
    },
    {
        "timestamp": "2025-08-26T14:43:23.758442",
        "game": "lotto",
        "selection": {
            "primary": [33,4,6,15,50,20],
            "primes_in_primary": []
        }
    },
    {
        "timestamp": "2025-08-26T14:43:23.762657",
        "game": "luckyday",
        "selection": {
            "primary": [14,15,24,28,31],
            "primes_in_primary": [31]
        }
    },
    {
        "timestamp": "2025-08-26T14:43:23.766733",
        "game": "pick3",
        "selection": {
            "primary": [8,0,9],
            "primes_in_primary": []
        }
    },
    {
        "timestamp": "2025-08-26T14:43:23.771511",
        "game": "pick4",
        "selection": {
            "primary": [2,3,5,7],
            "primes_in_primary": [2,3,5,7]
        }
    },
    {
        "timestamp": "2025-08-26T14:44:52.368500",
        "game": "megamillion",
        "selection": {
            "primary": [34,7,8,41,16],
            "primes_in_primary": [7,41],
            "mega": [18],
            "primes_in_mega": []
        }
    },
    {
        "timestamp": "2025-08-26T14:44:52.373475",
        "game": "powerball",
        "selection": {
            "primary": [65,34,9,43,22],
            "primes_in_primary": [43],
            "power": [11],
            "primes_in_power": [11]
        }
    },
    {
        "timestamp": "2025-08-26T14:44:52.379425",
        "game": "lotto",
        "selection": {
            "primary": [35,36,9,17,28,29],
            "primes_in_primary": [17,29]
        }
    },
    {
        "timestamp": "2025-08-26T14:44:52.384030",
        "game": "luckyday",
        "selection": {
            "primary": [34,45,15,26,30],
            "primes_in_primary": []
        }
    },
    {
        "timestamp": "2025-08-26T14:44:52.388771",
        "game": "pick3",
        "selection": {
            "primary": [2,5,6],
            "primes_in_primary": [2,5]
        }
    },
    {
        "timestamp": "2025-08-26T14:44:52.394812",
        "game": "pick4",
        "selection": {
            "primary": [8,1,4,9],
            "primes_in_primary": []
        }
    },
    {
        "timestamp": "2025-08-26T14:54:15.416747",
        "game": "megamillion",
        "selection": {
            "primary": [32,7,22,25,58],
            "primes_in_primary": [7],
            "mega": [1],
            "primes_in_mega": []
        }
    },
    {
        "timestamp": "2025-08-26T14:54:15.420272",
        "game": "powerball",
        "selection": {
            "primary": [10,50,23,27,61],
            "primes_in_primary": [23,61],
            "power": [13],
            "primes_in_power": [13]
        }
    },
    {
        "timestamp": "2025-08-26T14:54:15.425136",
        "game": "lotto",
        "selection": {
            "primary": [33,40,45,46,49,26],
            "primes_in_primary": []
        }
    },
    {
        "timestamp": "2025-08-26T14:54:15.428743",
        "game": "luckyday",
        "selection": {
            "primary": [34,5,6,44,30],
            "primes_in_primary": [5]
        }
    },
    {
        "timestamp": "2025-08-26T14:54:15.432476",
        "game": "pick3",
        "selection": {
            "primary": [8,9,5],
            "primes_in_primary": [5]
        }
    },
    {
        "timestamp": "2025-08-26T14:54:15.436439",
        "game": "pick4",
        "selection": {
            "primary": [0,3,6,7],
            "primes_in_primary": [3,7]
        }
    }
]
```
>- * ... and across potentially thousands of these records we need:
- Search Vertically by index: 
    - (e.g. look at position 0 of every primary list across all .jsons)
    - limit depth per array: - only consider up to index X in each array:
    - compute matches, frequencies, patterns, or cross‑game overlaps:
---
# Main Search Approaches:
### 1. Vertical Index Scan (Direct):
- Idea: is to iterate index by index, extract the Nth element from each relevant array, and process it.
    - Steps:
    - Choose which sequence you're focusing on (primary, mega, etc.):
    - Decide max index depth X:
    - For each index i from 0 --> X-1:
    - Traverse all jsons:
    - Collect the value at primary[i] - if it exists:
    - Aggregate, compare, or count as needed:

- Complexity:
    - Time: O(N × X)
    - (N = total JSON objects, X = positions scanned per array)

- Space: O(X) if we store per‑position counts.
- Use Case:
    - Best if we want exact counts or matches per position:

### 2. Vertical Index Scan (Direct):
- DP array: for Subsequence Matching:
    - If instead we want to detect vertical patterns, like:
        - "***Does number 47 appear at the same index across multiple games frequently ?***"

    - Then, DP can help:
        - We build a DP table:
        - `dp[i][num]` = frequency of num at index i
        - As we process each json, we increment counts:
            ```python
            dp[i][primary[i]] += 1
            ```
        - that should enable query mode for:
            - "***Which numbers are most common at index 0 across all games ?***"
            - "***Does [3,7] occur vertically aligned ?***"

- Complexity:
    - Preprocessing: O(N × X):
    - Query time: O(1) to O(k) depending on how many we feed to it:

### 3. Controlling Array Positions:
- Use Cases:
    - Shallow scan: X = 2 → Only look at the first two numbers of each primary:
    - Deep scan: X = len(primary) → Look at entire sequences:
    - Mixed scan: == different limits per game:
    ```python
    limits = {"megamillion": 5, "powerball": 5, "lotto": 6, "pick3": 3}
    ```
    This avoids over‑scanning arrays that are naturally short (e.g., Pick3 games):

### 4. Data Structure Design:
- To handle large datasets efficiently, we should pre‑compute a structure optimized for vertical queries:
    ```python
    vertical_index_map = {
        "primary": {
            0: Counter(),
            1: Counter(),
            2: Counter(),
            3: Counter(),
            4: Counter(),
        },
        "mega": {
            0: Counter()
        },
        "power": {
            0: Counter()
        }
    }
    ```
- ... so, as easch jsons gets loaded, we run loop and index them: 
    ```python
    for idx, num in enumerate(selection["primary"][:X]):
        vertical_index_map["primary"][idx][num] += 1
    ```

### 5. Algo Ideas/Options:
| Problem:	                             | Possible Algorithm choice	    | OS Resource Pressure                     |
| -------------------------------------- | ---------------------------------|------------------------------------------| 
| Find most common numbers per index:	 | Vertical DP table + Counters	    | `O(1)` queries after precompute:         |
| Check if specific sequence repeats:	 | Sliding window vertical scan	    | `O(N × X)` -- ? optimized by early exit ?|  
| Cross‑game vertical overlap:	         | Indexed hash map per index	    | `fast comparison` across games:          |
| Massive dataset optimization:	         | Bloom Filters + DP	            | negatives `skiped` instantly:            |
------------------------------------------ 

### Given repo's setup and data volume, a ***`dp + counter`*** should help ...
- went thorough this example -- [Mastering Dynamic Programming in Python: Solve 'Count All Possible Routes' Step by Step | 1575](https://www.youtube.com/watch?v=ZRO62QlYrZk)
- revisited this: -- [The Pythonic Way to Count Objects](https://realpython.com/python-counter/#:~:text=conveniently%20called%20Counter%20.-,Getting%20Started%20With%20Python's%20Counter,%2C%20'm':%201%7D)

```bash
Step #1 
    jsons stream -> watchthe buffer overaload:
    for each record_catalog:
        for each_key (primery, mega, power e.t.c):
            for item < limit:
            increment value count at index item: 
Step #2
 top N most commont numbers per each index:
 check IF a number or subsequence allings vertically:
 Compare overlap rates across all games: 
```

