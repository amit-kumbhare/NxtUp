"""
A2OJ Ladder Problem Fetcher
============================
Fetches problems from A2OJ Ladders 11, 16, and 19 (300 total)
and enriches each with rating + tags from the Codeforces API.

Output: sheet/sheet_problems/a2oj_problems.json
"""

import requests
import json
import re
import time
import os

# ── Config ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Absolute path to sheet/
LADDER_IDS = [11, 16, 19]          # ~100 problems each = 300 total
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "sheet_problems")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "a2oj_problems.json")

A2OJ_BASE  = "https://earthshakira.github.io/a2oj-clientside/server/Ladder{}.html"
CF_API_URL = "https://codeforces.com/api/problemset.problems"

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_cf_problem_map() -> dict:
    """
    Calls CF API once and returns a dict:
        (contestId, index) -> {title, contestId, index, rating, tags}
    """
    print("[1/3] Fetching all problems from Codeforces API...")
    resp = requests.get(CF_API_URL, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    if data["status"] != "OK":
        raise RuntimeError(f"CF API error: {data.get('comment', 'unknown')}")

    problem_map = {}
    for p in data["result"]["problems"]:
        if "contestId" not in p:
            continue
        key = (p["contestId"], p["index"])
        problem_map[key] = {
            "title":     p["name"],
            "contestId": p["contestId"],
            "index":     p["index"],
            "rating":    p.get("rating", None),   # null if CF hasn't rated it
            "tags":      p.get("tags", []),
        }

    print(f"    ✓ {len(problem_map)} problems loaded from CF API")
    return problem_map


def fetch_ladder_problem_ids(ladder_id: int) -> list[tuple[int, str]]:
    """
    Scrapes one A2OJ ladder page and returns a list of (contestId, index) tuples.
    """
    url = A2OJ_BASE.format(ladder_id)
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    # Links look like: /problemset/problem/69/A
    matches = re.findall(r"/problemset/problem/(\d+)/([A-Z]\d?)", resp.text)
    return [(int(cid), idx) for cid, idx in matches]


def fetch_all_ladder_ids(ladder_ids: list[int]) -> list[tuple[int, str]]:
    """
    Fetches problem IDs from all specified ladders, deduplicating across them.
    """
    print(f"[2/3] Scraping A2OJ ladders: {ladder_ids}")
    seen  = set()
    order = []

    for lid in ladder_ids:
        ids = fetch_ladder_problem_ids(lid)
        count_new = 0
        for key in ids:
            if key not in seen:
                seen.add(key)
                order.append(key)
                count_new += 1
        print(f"    Ladder {lid}: {len(ids)} problems found, {count_new} new after dedup")
        time.sleep(0.4)   # be polite to the server

    print(f"    ✓ {len(order)} unique problems across all ladders")
    return order


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    cf_map      = fetch_cf_problem_map()
    problem_ids = fetch_all_ladder_ids(LADDER_IDS)

    print("[3/3] Building enriched problem list...")
    problems  = []
    missing   = []

    for contest_id, index in problem_ids:
        key = (contest_id, index)
        if key in cf_map:
            problems.append(cf_map[key])
        else:
            missing.append(f"{contest_id}/{index}")

    if missing:
        print(f"    ⚠  {len(missing)} problems not found in CF API (possibly removed):")
        for m in missing:
            print(f"       - {m}")

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! {len(problems)} problems written to {OUTPUT_FILE}")
    print(f"   Rating distribution:")

    buckets = {}
    for p in problems:
        r = p["rating"]
        label = str(r) if r else "unrated"
        buckets[label] = buckets.get(label, 0) + 1
    for label, count in sorted(buckets.items()):
        print(f"     {label:>8}: {count} problems")


if __name__ == "__main__":
    main()