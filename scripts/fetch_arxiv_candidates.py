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
HF_LIMIT = 100
OUTPUT_ARXIV = Path("data/.arxiv_candidates.jsonl")
OUTPUT_HF = Path("data/.hf_top_papers.jsonl")
ATOM = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def parse_datetime(value: str) -> datetime:
    text = value.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc)


def fetch_arxiv(since_hours: float) -> list[dict]:
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
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            root = ET.fromstring(response.read())
    except Exception as exc:
        print(f"arXiv fetch failed: {exc}")
        return []

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
    return candidates


def fetch_hf_top() -> list[dict]:
    url = (
        "https://huggingface.co/api/papers"
        "?sort=upvotes&order=-1&date=30d"
        f"&limit={HF_LIMIT}"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "ai-surveys/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = json.load(response)
    except Exception as exc:
        print(f"Hugging Face papers fetch failed: {exc}")
        return []

    papers = []
    for item in raw:
        papers.append(
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "upvotes": item.get("upvotes"),
                "published_at": item.get("publishedAt"),
                "authors": [author.get("name") for author in item.get("authors", [])],
                "summary": item.get("summary"),
                "ai_summary": item.get("ai_summary"),
                "url": f"https://huggingface.co/papers/{item.get('id')}",
            }
        )
    return papers


def write_jsonl(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def main() -> int:
    since_hours = float(sys.argv[1]) if len(sys.argv) > 1 else 36.0
    candidates = fetch_arxiv(since_hours)
    write_jsonl(OUTPUT_ARXIV, candidates)

    hf_papers = fetch_hf_top()
    write_jsonl(OUTPUT_HF, hf_papers)

    print(f"Wrote {len(candidates)} arXiv candidates to {OUTPUT_ARXIV}")
    print(f"Wrote {len(hf_papers)} Hugging Face papers to {OUTPUT_HF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
