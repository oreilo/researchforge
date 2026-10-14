from __future__ import annotations
import time
from datetime import datetime, timezone
from urllib.parse import urlparse
import httpx
from .models import ResearchConfig, ResearchReport, ResearchSource
from .search import search
from .fetch import fetch_page
from .security import check_public_url, domain_allowed
from .analyze import relevance, select_evidence, build_findings

class ResearchEngine:
    def __init__(self, config: ResearchConfig, client: httpx.Client | None = None):
        self.config = config
        self.client = client

    def run(self) -> ResearchReport:
        c = self.config
        report = ResearchReport(topic=c.topic, questions=c.questions)
        owns_client = self.client is None
        client = self.client or httpx.Client(timeout=c.timeout_seconds, follow_redirects=False)
        try:
            queries = [c.topic] + c.questions[:5]
            hits = []
            for query in queries:
                try:
                    for attempt in range(3):
                        try:
                            hits.extend(search(query, c, client))
                            break
                        except (httpx.TimeoutException, httpx.TransportError):
                            if attempt == 2:
                                raise
                            time.sleep(0.3 * (2 ** attempt))
                except Exception as exc:
                    report.errors.append(f"Search for {query!r}: {type(exc).__name__}: {exc}")
            unique = {}
            for hit in hits:
                try:
                    url = check_public_url(hit.url)
                    if domain_allowed(url, c.allow_domains, c.block_domains):
                        unique.setdefault(url, hit)
                except ValueError as exc:
                    report.errors.append(f"Skipped unsafe search result: {exc}")
            report.metadata["search_hits"] = len(hits)
            report.metadata["unique_candidates"] = len(unique)
            for url, hit in list(unique.items())[:c.max_results]:
                if len(report.sources) >= c.max_pages:
                    break
                try:
                    page = fetch_page(url, client, agent=c.user_agent,
                                      max_chars=c.max_chars_per_page, respect_robots=c.respect_robots)
                    if not domain_allowed(page.url, c.allow_domains, c.block_domains):
                        raise ValueError("Redirect left allowed domains")
                    if len(page.text) < 80:
                        raise ValueError("Insufficient readable text")
                    report.sources.append(ResearchSource(
                        id=len(report.sources)+1, title=page.title, url=page.url,
                        domain=urlparse(page.url).hostname or "", retrieved_at=datetime.now(timezone.utc).isoformat(),
                        excerpt=select_evidence(page.text, c.topic), search_snippet=hit.snippet,
                        score=relevance(page.title + " " + page.text, c.topic)))
                except Exception as exc:
                    report.errors.append(f"Fetch {url}: {type(exc).__name__}: {exc}")
            report.sources.sort(key=lambda s: -s.score)
            for index, source in enumerate(report.sources, 1):
                source.id = index
            report.findings = build_findings(report.sources)
            report.summary = (f"Collected {len(report.sources)} accessible web sources for '{c.topic}'. "
                              "Findings below are extracted evidence, not independently verified conclusions.")
            if not report.sources:
                report.limitations.append("No accessible evidence was retrieved; do not treat this as a completed research report.")
            report.limitations.extend([
                "Source excerpts can be incomplete, inaccurate, outdated or contradictory.",
                "Relevance scores measure keyword overlap, not source credibility or factual accuracy.",
                "Search coverage depends on the configured search provider and website accessibility."])
            if c.ai_model and report.sources:
                try:
                    from .ai import synthesize
                    report.summary = synthesize(report, c.ai_model)
                    report.metadata["ai_synthesis"] = c.ai_model
                except Exception as exc:
                    report.errors.append(f"AI synthesis: {type(exc).__name__}: {exc}")
            return report
        finally:
            if owns_client:
                client.close()
