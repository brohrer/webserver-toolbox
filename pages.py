"""
Show the pages accessed on the webserver,
and how many each times each was hit.

Command line options

-d --domain   The log to analyze. Must be one of
    "com", "com1", "e2e", "tyr", "def", "test"
    Default: "com", for brandonrohrer.com, current day

-s --status  The http status code to focus on. Typically one of
    200: success
    301: redirected
    304: not modified (client should use it's cache)
    403: permission denied
    404: page not found
    Default: 200

Usage examples

- Show the current day's successful hits to brandonrohrer.com
    uv run pages

- Test against some stale data
    uv run pages.py --domain test

- Inspect the e2eml.school logs
    uv run pages.py --domain e2e

- Inspect the tyr.fyi logs
    uv run pages.py --domain tyr

- Find out which pages were sought, but not found
    uv run pages.py --status 404
"""

import argparse
import numpy as np
from targets import targets_to_ignore
import log_reader


# Ignore pages containing these substrings in their URL


def show_pages(domain="com", status_code="200"):
    log_df = log_reader.get_logs(domain)
    pages_visited = (
        log_df.loc[log_df["code"] == status_code, "uri"]
        .str.removesuffix(".html")
        .values
    )

    pages, counts = np.unique(pages_visited, return_counts=True)
    order = np.argsort(counts)
    for i in order:
        if pages[i] in targets_to_ignore:
            continue
        print(counts[i], pages[i])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="com", required=False)
    parser.add_argument("-s", "--status", default="200", required=False)
    args = parser.parse_args()

    show_pages(domain=args.domain, status_code=args.status)
