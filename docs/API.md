# HTTP API

Install `pip install -e ".[server]"` and set `RESEARCHFORGE_API_KEY` to a long random value. Run `uvicorn oreilo_researchforge.asgi:app --reload` for local development.

- `GET /health` - no authentication; liveness only.
- `POST /projects` - JSON `{ "title": "Project name" }`.
- `GET /projects` - list projects.
- `POST /projects/{project_id}/research` - JSON `ResearchConfig`; synchronous research, returns report and run ID.
- `GET /runs/{run_id}` - persisted status and report.

Authenticated routes require `X-API-Key`. For internet-facing production, configure HTTPS, network policy, reverse proxy rate limiting, and tenant isolation before deployment.
