# Architecture

ResearchForge v2 layers:

1. `planning` creates explicit research questions and search queries.
2. Existing `search`, `fetch`, `security`, `pipeline` collect source excerpts; domain policy and SSRF checks apply to the original network pipeline.
3. `evidence`, `quality`, `graph`, `intelligence` create inspectable research artifacts. Their lexical signals are **not** factual verification.
4. `documents` and `retrieval` support local ingestion and BM25-style keyword retrieval. Vector search is not implemented.
5. `storage` persists projects and completed reports in SQLite.
6. `service` provides an authenticated FastAPI interface. Jobs run synchronously; do not treat it as a distributed worker queue.
7. `exports_plus` supports additional file formats; the base `export` module remains available.
8. `orchestrator` is a generic stage runner with trace events; existing research pipeline is not yet implemented as a fully autonomous multi-agent loop.

## Security considerations

Never expose the API without `RESEARCHFORGE_API_KEY`. Default Compose binds to localhost. Treat researched websites and document contents as untrusted. The search backend may require its own deployment. Do not allow untrusted clients to choose arbitrary server-side file paths. Deploy behind a TLS reverse proxy and an authorization gateway for multi-user use.

## Gaps

No autonomous agent delegation, no distributed background jobs, no vector database, no independently verified fact-checking, no live provider integration testing, no production-grade multi-tenancy. These require separate engineering and testing.
