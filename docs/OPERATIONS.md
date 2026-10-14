# Operations and validation

```bash
python -m pip install -e ".[dev,server,documents]"
python -m pytest -q
researchforge plan "open source AI governance"
researchforge document-search notes.md "governance"
researchforge project-create "My research"
export RESEARCHFORGE_API_KEY="replace-with-long-random-secret"
uvicorn oreilo_researchforge.asgi:app --reload
```

Live research requires a working configured SearXNG or Serper provider. Without a provider, tests validate deterministic components only. Set secrets through environment variables; never commit them. PDF extraction requires selectable text; OCR is not provided. Research reports are not a substitute for independent source review.
