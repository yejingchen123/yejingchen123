#!/usr/bin/env python3
"""Refresh the profile from the public blog RSS feed; standard library only."""

import re
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FEED_URL = "https://yejingchen123.github.io/rss.xml"


def markdown_text(value):
    """Treat feed titles as plain text, never injected Markdown or HTML."""
    value = " ".join(value.split())
    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"([\\`*_{}\[\]()!|])", r"\\\1", value)


def entries_from_feed(xml):
    root = ET.fromstring(xml)
    entries = []
    for item in root.findall("./channel/item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        parts = urlsplit(link)
        if not title or parts.scheme != "https" or parts.netloc != "yejingchen123.github.io":
            continue
        if any(char in link for char in "<>\r\n\t "):
            continue
        published = parsedate_to_datetime(item.findtext("pubDate", ""))
        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)
        entries.append((published, title, link))
    entries.sort(key=lambda item: item[0], reverse=True)
    if not entries:
        raise ValueError("The feed has no valid published entries; keep the previous README.")
    return [f"- `{date:%Y-%m-%d}` &nbsp; [{markdown_text(title)}](<{link}>)" for date, title, link in entries[:4]]


def main():
    request = Request(FEED_URL, headers={"User-Agent": "yejingchen123-profile"})
    with urlopen(request, timeout=30) as response:
        xml = response.read(2_000_001)
    if len(xml) > 2_000_000:
        raise ValueError("Unexpectedly large RSS response")
    entries = entries_from_feed(xml)
    path = ROOT / "README.md"
    content = path.read_text(encoding="utf-8")
    start, end = "<!-- BLOG:START -->", "<!-- BLOG:END -->"
    if content.count(start) != 1 or content.count(end) != 1:
        raise ValueError("Expected exactly one pair of blog markers")
    before, rest = content.split(start, 1)
    _, after = rest.split(end, 1)
    updated = before + start + "\n" + "\n".join(entries) + "\n" + end + after
    if updated != content:
        path.write_text(updated, encoding="utf-8")
    print(f"Blog entries checked: {len(entries)}")


if __name__ == "__main__":
    main()
