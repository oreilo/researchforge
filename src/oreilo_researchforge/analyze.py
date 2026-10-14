"""Deterministic, citation-preserving extraction; optional AI synthesis elsewhere."""
from __future__ import annotations
import re
from collections import Counter
from urllib.parse import urlparse
from .models import ResearchSource

STOP = set("about after again also been before being between could every first from have into more most other over same some such than that their them there these they this those through under very were what when where which while with would your".split())

def terms(text: str) -> list[str]:
    return [x for x in re.findall(r"[a-zA-Z][a-zA-Z0-9-]{2,}", text.lower()) if x not in STOP]

def relevance(text: str, query: str) -> float:
    keys = set(terms(query))
    if not keys:
        return 0
    sample = Counter(terms(text[:15000]))
    return round(sum(min(sample[k], 5) for k in keys) / (5 * len(keys)), 3)

def select_evidence(text: str, query: str, limit: int = 500) -> str:
    segments = re.split(r"(?<=[.!?])\s+", text)
    keys = set(terms(query))
    ranked = sorted(enumerate(segments), key=lambda it: (-len(keys.intersection(terms(it[1]))), it[0]))
    chosen = [s.strip() for _, s in ranked if len(s.strip()) > 25][:3]
    return " ".join(chosen)[:limit] or text[:limit]

def build_findings(sources: list[ResearchSource], limit: int = 10) -> list[str]:
    return [f"{s.excerpt} [{s.id}]" for s in sorted(sources, key=lambda x: -x.score)[:limit] if s.excerpt]
