from __future__ import annotations
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class ResearchConfig(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    questions: list[str] = Field(default_factory=list)
    max_results: int = Field(default=12, ge=1, le=100)
    max_pages: int = Field(default=10, ge=1, le=50)
    max_chars_per_page: int = Field(default=12000, ge=500, le=100000)
    timeout_seconds: float = Field(default=12, ge=2, le=120)
    allow_domains: list[str] = Field(default_factory=list)
    block_domains: list[str] = Field(default_factory=list)
    respect_robots: bool = True
    user_agent: str = "OREiLO-ResearchForge/1.0 (+https://oreilo.com)"
    search_backend: str = "searxng"
    searxng_url: str = "http://localhost:8080"
    language: str = "en"
    ai_model: str | None = None

class SearchHit(BaseModel):
    title: str
    url: str
    snippet: str = ""
    engine: str = ""

class ResearchSource(BaseModel):
    id: int
    title: str
    url: str
    domain: str
    excerpt: str
    retrieved_at: str
    search_snippet: str = ""
    score: float = 0

class ResearchReport(BaseModel):
    topic: str
    questions: list[str]
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    summary: str = ""
    findings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    sources: list[ResearchSource] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
