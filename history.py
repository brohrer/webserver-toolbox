"""
Show the webserver's logs in an easier to read format.

Usage examples

- Show the current day's hits to brandonrohrer.com
    uv run history.py

- Show the hits from a particular IP address
    uv run history.py --ip 123.123.123.123

- Test against some stale data
    uv run history.py --domain test

- Inspect the e2eml.school logs
    uv run history.py --domain e2e

- Inspect the tyr.fyi logs
    uv run history.py --domain tyr

- Show the requests for GET requests only
    uv run history.py --action GET

- Show the requests for all requests *except* GET requests
    uv run history.py --notaction GET


`targets_to_ignore` is a list of URLs that are uninteresting
and shouldn't be displayed.
"""

import argparse
from targets import targets_to_ignore
import log_reader


def show_history(
    domain="com",
    action=None,
    ip=None,
    notaction=None,
    status=None,
):
    """
    domain: str
        One of {"com", "com1", "e2e", "tyr", "def", "test"}.
        Specify which domain to show logs for, for example
        "com" = brandonrohrer.com
        "test" = a test log for development

    action: str
        An HTTP action, for example {"GET", "POST", "HEAD", "DELETE"}.
        Only show access events for HTTP requests of a particular type.

    ip: str
        Show all the requests from a particular IP address.

    notaction: str
        Just like the `action` argument, but show everything *except*
        this action.

    status: str
        An HTTP status code, for example {"200", "301", "404", "429", "503"}.
        Only show requests with this code.
    """
    log_df = log_reader.get_logs(domain)
    for i, row in log_df.iterrows():
        if action is not None:
            if row["action"].lower() != action.lower():
                continue
        if ip is not None:
            if row["ip"] != ip:
                continue
        if notaction is not None:
            if row["action"].lower() == notaction.lower():
                continue
        if status is not None:
            if row["code"] != status:
                continue
        # Ignore some common ones
        if row["uri"] not in targets_to_ignore:
            print(
                f"{row['hour']}:{row['minute']}:{row['second']}  "
                + f"{row['action']} "
                + f"{row['code']} "
                + f"{row['ip']} "
                + f"{row['uri']}"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", default="com", required=False)
    parser.add_argument("--ip", default=None)
    parser.add_argument("-s", "--status", default=None)
    parser.add_argument("-a", "--action", default=None)
    parser.add_argument("-n", "--notaction", default=None)
    args = parser.parse_args()

    show_history(
        domain=args.domain,
        action=args.action,
        ip=args.ip,
        notaction=args.notaction,
        status=args.status,
    )
