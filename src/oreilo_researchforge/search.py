"""Pluggable search engines: SearXNG (self-hosted) and Serper (API key)."""
from __future__ import annotations
import os
import httpx
from .models import SearchHit, ResearchConfig

class SearchError(RuntimeError):
    pass

def search(query: str, config: ResearchConfig, client: httpx.Client) -> list[SearchHit]:
    if config.search_backend == "searxng":
        response = client.get(config.searxng_url.rstrip("/") + "/search", params={
            "q": query, "format": "json", "language": config.language,
        })
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
            raise SearchError("Invalid SearXNG JSON response; enable JSON format in SearXNG settings")
        return [SearchHit(title=str(r.get("title", "Untitled")), url=r["url"],
                          snippet=str(r.get("content", "")), engine="searxng")
                for r in payload["results"] if isinstance(r, dict) and r.get("url")]
    if config.search_backend == "serper":
        key = os.getenv("SERPER_API_KEY")
        if not key:
            raise SearchError("Set SERPER_API_KEY in your environment")
        response = client.post("https://google.serper.dev/search", headers={"X-API-KEY": key},
                               json={"q": query, "num": min(config.max_results, 100)})
        response.raise_for_status()
        return [SearchHit(title=str(r.get("title", "Untitled")), url=r["link"],
                          snippet=str(r.get("snippet", "")), engine="serper")
                for r in response.json().get("organic", []) if r.get("link")]
    raise SearchError("search_backend must be searxng or serper")
