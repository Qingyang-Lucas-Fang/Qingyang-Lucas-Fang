#!/usr/bin/env python3
"""Render genuine public GitHub statistics. Python stdlib only; no chart service."""

import json
import os
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = os.environ.get("PROFILE_OWNER", "Qingyang-Lucas-Fang")
TOKEN = os.environ.get("GH_TOKEN", "")
LANGUAGE_COLORS = {"Python": "#63CBA7", "Jupyter Notebook": "#F5AE8E", "TypeScript": "#79A9E9", "JavaScript": "#D5C76E", "HTML": "#E38E77", "CSS": "#A6A0E5", "C++": "#C889B2", "C": "#8EA5B4", "Shell": "#AFCB89", "Other": "#87939E"}


def read_url(url, payload=None):
    headers = {"User-Agent": "Lucas-Fang-Profile", "Accept": "application/vnd.github+json"}
    # Never forward credentials to a non-API host, including GitHub's HTML pages.
    if TOKEN and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    with urlopen(Request(url, data=data, headers=headers), timeout=40) as response:
        return response.read().decode("utf-8")


def api(path):
    return json.loads(read_url("https://api.github.com" + path))


def owned_repositories(owner):
    repos = []
    page = 1
    while True:
        batch = api(f"/users/{owner}/repos?type=owner&per_page=100&page={page}")
        repos.extend(r for r in batch if not r["fork"] and not r.get("private", False) and r["owner"]["login"].casefold() == owner.casefold())
        if len(batch) < 100:
            return repos
        page += 1


class ContributionParser(HTMLParser):
    """Read only public dates, levels and labels from GitHub's calendar."""

    def __init__(self):
        super().__init__()
        self.days = {}
        self.ids = {}
        self.heading = False
        self.heading_text = ""
        self.tooltip = None
        self.tooltip_text = ""
        self.total = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h2" and attrs.get("id") == "js-contribution-activity-description":
            self.heading = True
        if tag == "td" and "data-date" in attrs and "data-level" in attrs:
            day = date.fromisoformat(attrs["data-date"]).isoformat()
            level = int(attrs["data-level"])
            if not 0 <= level <= 4:
                raise ValueError("Unexpected contribution level")
            self.days[day] = {"date": day, "level": level, "count": None}
            self.ids[attrs.get("id")] = day
        if tag == "tool-tip" and attrs.get("for") in self.ids:
            self.tooltip = self.ids[attrs["for"]]
            self.tooltip_text = ""

    def handle_data(self, data):
        if self.heading:
            self.heading_text += data
        if self.tooltip:
            self.tooltip_text += data

    def handle_endtag(self, tag):
        if tag == "h2" and self.heading:
            match = re.search(r"([\d,]+)\s+contributions?", self.heading_text)
            if match:
                self.total = int(match[1].replace(",", ""))
            self.heading = False
        if tag == "tool-tip" and self.tooltip:
            match = re.search(r"(No|[\d,]+)\s+contributions?", self.tooltip_text)
            if match:
                self.days[self.tooltip]["count"] = 0 if match[1] == "No" else int(match[1].replace(",", ""))
            self.tooltip = None


def contributions(owner):
    if TOKEN:
        query = """query($login:String!) { user(login:$login) { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount contributionLevel } } } } } }"""
        try:
            response = json.loads(read_url("https://api.github.com/graphql", {"query": query, "variables": {"login": owner}}))
            if response.get("errors"):
                raise ValueError("Contribution API unavailable for this token")
            calendar = response["data"]["user"]["contributionsCollection"]["contributionCalendar"]
            levels = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
            days = [{"date": d["date"], "count": d["contributionCount"], "level": levels[d["contributionLevel"]]} for w in calendar["weeks"] for d in w["contributionDays"]]
            if not days:
                raise ValueError("Contribution API returned no calendar days")
            return {"total": calendar["totalContributions"], "days": days}
        except (HTTPError, URLError, TimeoutError, KeyError, TypeError, ValueError):
            print("GraphQL calendar unavailable; trying GitHub's public calendar.", file=sys.stderr)
    try:
        parser = ContributionParser()
        parser.feed(read_url(f"https://github.com/users/{owner}/contributions"))
        if parser.total is None or len(parser.days) < 300:
            raise ValueError("Public contribution-calendar markup was not recognized")
        return {"total": parser.total, "days": sorted(parser.days.values(), key=lambda d: d["date"])}
    except (HTTPError, URLError, TimeoutError, ValueError):
        print("Contribution data unavailable; the panel will label it accordingly.", file=sys.stderr)
        return None


def label(x, y, value, size, color, weight=400, mono=False, extra=""):
    font = "'SFMono-Regular',Consolas,'Liberation Mono',monospace" if mono else "Arial,Helvetica,sans-serif"
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(str(value))}</text>'


def render(data, dark):
    bg, fg, muted, border = ("#101820", "#F5F2EA", "#A7B7C3", "#2A3A46") if dark else ("#F8F7F2", "#20313A", "#596C74", "#D9DFD8")
    accent = "#9BF0CD" if dark else "#246C56"
    colors = ["#1E3038", "#245846", "#347D5D", "#65B993", "#9BF0CD"] if dark else ["#E3E8E1", "#C4E1D2", "#8BC5AB", "#4B9D7D", "#266F55"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="482" viewBox="0 0 1200 482" role="img" aria-labelledby="title desc">', '<title id="title">Lucas Fang — public GitHub activity</title>']
    cal = data["calendar"]
    contribution_desc = f'{cal["total"]:,} contributions in the last year.' if cal else "Contribution data currently unavailable."
    parts.append(f'<desc id="desc">{data["repo_count"]} owned public non-fork repositories. {data["stars"]} stars across those repositories. {data["followers"]} followers. {contribution_desc} Updated {data["updated"]}.</desc>')
    parts.append(f'<rect x="1" y="1" width="1198" height="480" rx="14" fill="{bg}" stroke="{border}"/>')
    parts.append(label(40, 37, "GITHUB / FIELD NOTES", 12, accent, mono=True, extra='letter-spacing="1.8"'))
    parts.append(label(1160, 37, f'UPDATED {data["updated"]}', 11, muted, mono=True, extra='text-anchor="end"'))
    parts.append(f'<path d="M40 61H1160 M40 187H1160 M40 390H1160" stroke="{border}"/>')
    metrics = [(40, data["repo_count"], "ORIGINAL PUBLIC REPOS"), (333, data["stars"], "STARS · THOSE REPOS"), (626, data["followers"], "FOLLOWERS"), (919, cal["total"] if cal else "—", "CONTRIBUTIONS · 12 MO")]
    for x, value, title in metrics:
        parts.append(label(x, 130, f"{value:,}" if isinstance(value, int) else value, 51, fg, 700, extra='letter-spacing="-2"'))
        parts.append(label(x, 162, title, 11, muted, mono=True))
    if cal:
        days = sorted(cal["days"], key=lambda d: d["date"])
        first, last = date.fromisoformat(days[0]["date"]), date.fromisoformat(days[-1]["date"])
        start = first - timedelta(days=(first.weekday() + 1) % 7)
        columns = (last - start).days // 7 + 1
        step = min(20, 1080 / columns)
        cell = min(14, step - 4)
        parts.append(label(40, 271, "M", 10, muted, mono=True))
        parts.append(label(40, 311, "W", 10, muted, mono=True))
        parts.append(label(40, 351, "F", 10, muted, mono=True))
        month_positions = {}
        for day in days:
            when = date.fromisoformat(day["date"])
            column = (when - start).days // 7
            row = (when.weekday() + 1) % 7
            x, y = 72 + column * step, 237 + row * 20
            count = day.get("count")
            tooltip = f'{when.isoformat()}: {count} contributions' if count is not None else f'{when.isoformat()}: activity level {day["level"]}/4'
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{cell:.1f}" height="14" rx="3" fill="{colors[day["level"]]}"><title>{escape(tooltip)}</title></rect>')
            if when.day == 1 or when == first:
                month_positions[(when.year, when.month)] = (x, when.strftime("%b"))
        previous = -100
        for x, month in month_positions.values():
            if x - previous > 40:
                parts.append(label(f"{x:.1f}", 220, month, 11, muted, mono=True))
                previous = x
        parts.append(label(880, 377, "LESS", 9, muted, mono=True))
        for i, color in enumerate(colors):
            parts.append(f'<rect x="{920+i*19}" y="367" width="12" height="12" rx="2" fill="{color}"/>')
        parts.append(label(1022, 377, "MORE", 9, muted, mono=True))
    else:
        parts.append(label(40, 263, "Contribution calendar unavailable", 22, fg, 600))
        parts.append(label(40, 298, "Repository statistics above are current. The calendar will retry on the next refresh.", 16, muted))
    languages = data["languages"]
    total = sum(languages.values())
    ordered = sorted(languages.items(), key=lambda x: (-x[1], x[0]))
    shown = ordered[:3]
    if len(ordered) > 3:
        shown.append(("Other", sum(v for _, v in ordered[3:])))
    parts.append(label(40, 417, "REPOSITORY LANGUAGES / BY SOURCE BYTES", 10, muted, mono=True))
    if total:
        x = 40.0
        for lang, count in shown:
            width = count / total * 1120
            parts.append(f'<rect x="{x:.2f}" y="429" width="{width:.2f}" height="8" fill="{LANGUAGE_COLORS.get(lang, LANGUAGE_COLORS["Other"])}"/>')
            x += width
        legend_x = 40
        for lang, count in shown:
            color = LANGUAGE_COLORS.get(lang, LANGUAGE_COLORS["Other"])
            percent = count / total * 100
            pct_label = "<0.1%" if percent < 0.1 else f"{percent:.1f}%"
            parts.append(f'<circle cx="{legend_x+4}" cy="458" r="4" fill="{color}"/>')
            value = f"{lang} {pct_label}"
            parts.append(label(legend_x + 17, 462, value, 12, muted))
            legend_x += max(190, len(value) * 7 + 46)
    else:
        parts.append(label(40, 458, "No public source-language data available.", 12, muted))
    parts.append("</svg>\n")
    return "\n".join(parts)


def main():
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", OWNER):
        raise ValueError("PROFILE_OWNER must be a GitHub username")
    user = api(f"/users/{OWNER}")
    repos = owned_repositories(OWNER)
    languages = Counter()
    for repo in repos:
        languages.update(api(f'/repos/{OWNER}/{repo["name"]}/languages'))
    data = {"repo_count": len(repos), "stars": sum(r["stargazers_count"] for r in repos), "followers": user["followers"], "languages": dict(languages), "calendar": contributions(OWNER), "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
    # Complete all network reads and renders before replacing the checked-in panels.
    rendered = {name: render(data, dark) for name, dark in [("activity-dark.svg", True), ("activity-light.svg", False)]}
    output = ROOT / "assets"
    output.mkdir(exist_ok=True)
    for name, content in rendered.items():
        temporary = output / (name + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(output / name)
    print(json.dumps({k: v for k, v in data.items() if k != "calendar"}, indent=2))
    print("Contribution calendar:", f'{data["calendar"]["total"]:,} contributions' if data["calendar"] else "unavailable")


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError) as error:
        # Do not print response bodies or request headers, which could contain credentials.
        print(f"Profile refresh failed ({type(error).__name__}); existing panels were retained.", file=sys.stderr)
        sys.exit(1)
