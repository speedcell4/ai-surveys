#!/usr/bin/env python3
"""Fetch recent arXiv metadata and write a candidate JSONL for Codex to triage."""

import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path


CATEGORIES = ["cs.CL", "cs.LG", "cs.CV", "cs.AI"]
MAX_RESULTS = 300
OUTPUT = Path("data/.arxiv_candidates.jsonl")
ATOM = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def parse_datetime(value: str) -> datetime:
    text = value.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc)


def main() -> int:
    since_hours = float(sys.argv[1]) if len(sys.argv) > 1 else 36.0
    cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)

    query = " OR ".join(f"cat:{cat}" for cat in CATEGORIES)
    params = {
        "search_query": query,
        "start": 0,
        "max_results": MAX_RESULTS,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(url, headers={"User-Agent": "ai-surveys/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        root = ET.fromstring(response.read())

    candidates = []
    for entry in root.findall("atom:entry", ATOM):
        title = " ".join((entry.findtext("atom:title", "", ATOM) or "").split())
        summary = " ".join((entry.findtext("atom:summary", "", ATOM) or "").split())
        arxiv_id = entry.findtext("atom:id", "", ATOM) or ""
        published = entry.findtext("atom:published", "", ATOM) or ""
        updated = entry.findtext("atom:updated", "", ATOM) or ""
        link = ""
        for node in entry.findall("atom:link", ATOM):
            if node.attrib.get("rel") == "alternate":
                link = node.attrib.get("href", "")
                break
        categories = [node.attrib.get("term", "") for node in entry.findall("atom:category", ATOM)]

        updated_dt = parse_datetime(updated)
        if updated_dt < cutoff:
            continue

        candidates.append(
            {
                "id": arxiv_id,
                "title": title,
                "abstract": summary,
                "published": published,
                "updated": updated,
                "url": link,
                "categories": categories,
            }
        )

    candidates.sort(key=lambda item: item["updated"], reverse=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as handle:
        for item in candidates:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Wrote {len(candidates)} candidates to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
