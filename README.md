# OREiLO ResearchForge v2.0

**An open-source, evidence-first web research and reporting toolkit by OREiLO.**

ResearchForge helps developers gather website evidence, manage research projects, inspect sources, ingest local documents, run structured research workflows and export reports. It prioritizes traceability and makes no unsupported claims of automated fact verification.

## What works

- Search-provider-driven web research through the existing SearXNG/Serper adapters; safe URL checks, domain controls, retries and robots policy.
- Structured research plans, question coverage, source-backed excerpts and an auditable evidence ledger.
- Lightweight entity co-occurrence graph, quality metrics and source diversity breakdowns.
- TXT, Markdown, CSV, JSON, HTML ingestion; optional PDF, DOCX, XLSX support.
- Local document chunking and BM25-inspired keyword ranking.
- Persistent SQLite projects, runs and research report history.
- Generic multi-stage orchestration with retry and execution traces.
- Markdown/HTML/JSON reports plus CSV, DOCX and PDF exports (optional dependencies).
- Python SDK, CLI, authenticated FastAPI, Docker Compose, CI tests.
- Optional AI-assisted synthesis with a configured compatible model.

## Install

```bash
python -m pip install -e ".[dev,server,documents,ai]"
python -m pytest -q
researchforge --help
```

## Quick start - no external services

```bash
researchforge plan "AI adoption in small businesses"
researchforge document-search README.md "evidence"
researchforge project-create "Market intelligence"
researchforge project-list
```

## Live web research

```bash
researchforge research "semiconductor packaging trends" --backend searxng --searxng-url http://localhost:8080 --max-pages 8 --output report.md
```

A running SearXNG server (or configured alternative) and network access are required. Live web results are **not** tested by the offline test suite.

## Python SDK

```python
from oreilo_researchforge.models import ResearchConfig
from oreilo_researchforge.pipeline import ResearchEngine
from oreilo_researchforge.intelligence import enrich

report = ResearchEngine(ResearchConfig(topic="battery recycling", max_pages=5)).run()
artifacts = enrich(report)
print(report.summary)
print(artifacts["quality"])
```

## API and Docker

```bash
python -m pip install -e ".[server]"
export RESEARCHFORGE_API_KEY="replace-with-long-random-secret"
uvicorn oreilo_researchforge.asgi:app --host 127.0.0.1 --port 8000
```

On Windows PowerShell: `$env:RESEARCHFORGE_API_KEY="replace-with-long-random-secret"`.

See `docs/API.md`, `docs/ARCHITECTURE.md`, `docs/OPERATIONS.md`.

## Honest boundaries

This release does **not** implement fully autonomous multi-agent research, independent factual verification, distributed queues, recurring scheduling, production multi-tenancy, semantic vector search, or arbitrary credentialed browser automation. Evidence scores and lexical coverage do not establish truth. Research findings require source review. Server research endpoints run synchronously.

## License

MIT License. Personal and commercial use, modification, and redistribution are permitted subject to the license terms.

Copyright (c) 2026 OREiLO.

## Commercial development and support

OREiLO provides custom integrations, deployment, research workflow development, and maintenance.

Contact: contact@oreilo.com | Website: https://oreilo.com
