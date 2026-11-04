#!/usr/bin/env python3
"""
Pull comments from Reddit threads into a CSV for labelling.

    python collect.py THREAD_URL_OR_FILE [...] --out raw_posts.csv

Uses Reddit's public .json view of a thread — no account, no key. If Reddit
blocks the request (403), open the thread URL with ".json" on the end in your
browser, save the page as a file, and pass the file path instead. Writes
text/label/note columns with label left blank, so the file can be labelled
and then copied into labels.csv. Running it again appends new threads and
skips posts already in the file.
"""

import argparse
import html
import json
import os
import sys
import time

import pandas as pd
import requests

HEADERS = {"User-Agent": "takemeter-collector/0.1 (class project)"}
MIN_WORDS = 4  # shorter than this is almost never labellable


def thread_json_url(url):
    url = url.split("?")[0].rstrip("/")
    return url + ".json?limit=500&depth=10&sort=top"


def walk(children, out):
    for child in children:
        if child.get("kind") != "t1":
            continue  # skip "load more" stubs
        data = child["data"]
        body = html.unescape(data.get("body", "")).strip()
        if body and body not in ("[deleted]", "[removed]") \
                and data.get("author") != "AutoModerator":
            out.append(body)
        replies = data.get("replies")
        if isinstance(replies, dict):
            walk(replies["data"]["children"], out)


def fetch(url):
    if os.path.exists(url):  # a thread's .json saved from the browser
        with open(url, encoding="utf-8") as f:
            post, comments = json.load(f)
    else:
        resp = requests.get(thread_json_url(url), headers=HEADERS, timeout=30)
        resp.raise_for_status()
        post, comments = resp.json()
    out = []
    walk(comments["data"]["children"], out)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--out", default="raw_posts.csv")
    args = parser.parse_args()

    existing = pd.read_csv(args.out) if os.path.exists(args.out) \
        else pd.DataFrame(columns=["text", "label", "note"])
    seen = set(existing["text"])

    rows = []
    for url in args.urls:
        try:
            bodies = fetch(url)
        except requests.RequestException as e:
            print(f"[skip] {url}: {e}", file=sys.stderr)
            continue
        kept = 0
        for body in bodies:
            if len(body.split()) < MIN_WORDS or body in seen:
                continue
            seen.add(body)
            rows.append({"text": body, "label": "", "note": ""})
            kept += 1
        print(f"{kept:4d} new of {len(bodies):4d} comments  {url}")
        time.sleep(2)  # be polite to Reddit

    combined = pd.concat([existing, pd.DataFrame(rows)], ignore_index=True)
    combined.to_csv(args.out, index=False)
    print(f"{len(combined)} posts in {args.out}")


if __name__ == "__main__":
    main()
