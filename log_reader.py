import pandas as pd

_show_history = True
_show_ips = False
_show_pages = False
_show_404s = False
_show_referrers = False
_referrers_page = "/"
_show_ip = True
_ip = "217.113.194.191"

logfiles = {
    "com": "/var/log/nginx/brandonrohrer.com/access.log",
    "com1": "/var/log/nginx/brandonrohrer.com/access.log.1",
    "e2e": "/var/log/nginx/e2eml.school/access.log",
    "tyr": "/var/log/nginx/tyr.fyi/access.log",
    "def": "/var/log/nginx/access.log",
    "test": "test.log",
}


def get_logs(domain="com"):
    pd.set_option("display.max_rows", None)
    with open(logfiles[domain], "rt") as f:
        log = f.readlines()

    rowlist = []
    for entry in log:
        i_left_bracket = entry.find("[")
        i_right_bracket = entry.find("]")
        datetimetzstr = entry[i_left_bracket + 1 : i_right_bracket]
        datetimestr, tz = datetimetzstr.split(" ")
        datestr = datetimestr[:11]
        timestr = datetimestr[12:]
        day = datestr[:2]
        month = datestr[3:6]
        year = datestr[7:]
        hour = timestr[:2]
        minute = timestr[3:5]
        second = timestr[6:]

        predate_content = entry[: i_left_bracket - 1]
        postdate_content = entry[i_right_bracket + 3 :]

        ip, some_stuff, more_stuff = predate_content.split(" ")

        parts = postdate_content.split('"')
        try:
            action, uri, protocol = parts[0].split(" ")
        except ValueError:
            action = ""
            uri = ""
            protocol = ""
        code, body_bytes = parts[1].strip().split(" ")
        referrer = parts[2]
        # empty = parts[3]
        agent = parts[4]

        row = {
            "code": code,
            "uri": uri,
            "ip": ip,
            "action": action,
            "referrer": referrer,
            "body_bytes": body_bytes,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "tz": tz,
            "protocol": protocol,
            "agent": agent,
        }
        rowlist.append(row)

    log_df = pd.DataFrame(rowlist)

    return log_df


if __name__ == "__main__":
    logs = get_logs(domain="test")
    print(logs.head())
