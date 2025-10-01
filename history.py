"""
Show the webserver's logs in an easier to read format.

Usage examples

- Show the current day's hits to brandonrohrer.com
    uv run history

- Show the hits from a particular IP address
    uv run history --ip 123.123.123.123

- Test against some stale data
    uv run history --domain test

- Inspect the e2eml.school logs
    uv run history --domain e2e

- Inspect the tyr.fyi logs
    uv run history --domain tyr


`targets_to_ignore` is a list of URLs that are uninteresting
and shouldn't be displayed.
"""
import argparse
import log_reader

targets_to_ignore = [
    "/apple-touch-icon-120x120.png",
    "/apple-touch-icon-120x120-precomposed.png",
    "/apple-touch-icon.png",
    "/apple-touch-icon-precomposed.png",
    "/favicon.ico",
    "/images/ml_logo.png",
    "/javascripts/blog_head.js",
    "/javascripts/blog_header.js",
    "/javascripts/blog_signature.js",
    "/javascripts/blog_footer.js",
    "robots.txt",
    "/sitemap.xml",
    "/stylesheets/stylesheet.css",
    "/stylesheets/print.css",
    "/.well-known/traffic-advice",
]

# domains = ["com", "com1", "e2e", "tyr", "def", "test"] 


def show_history(domain="com", ip=None):
    log_df = log_reader.get_logs(domain)
    for i, row in log_df.iterrows():
        if ip is not None:
            if row['ip'] != ip:
                continue
        # Ignore some common ones
        if row['uri'] not in targets_to_ignore:
            print(f"{row['hour']}:{row['minute']} {row['code']} {row['ip']} {row['uri']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="com", required=False)
    parser.add_argument("--ip", default=None)
    args = parser.parse_args()

    show_history(domain=args.domain, ip=args.ip)
