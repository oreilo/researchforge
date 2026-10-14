from __future__ import annotations
import json
from pathlib import Path
from html import escape
from .models import ResearchReport

def markdown(report: ResearchReport) -> str:
    lines = [f"# Research Report: {report.topic}", "", f"Generated: {report.created_at}", "", "## Executive summary", "", report.summary, "", "## Research questions", ""]
    lines += [f"- {q}" for q in report.questions] or ["- General overview"]
    lines += ["", "## Evidence and findings", ""]
    lines += [f"{i}. {finding}" for i, finding in enumerate(report.findings, 1)] or ["No verified evidence available."]
    lines += ["", "## Sources", ""]
    lines += [f"[{s.id}] {s.title} - {s.url} (relevance: {s.score:.2f}; accessed: {s.retrieved_at})" for s in report.sources] or ["No sources retrieved."]
    lines += ["", "## Limitations", ""]
    lines += [f"- {x}" for x in report.limitations]
    if report.errors:
        lines += ["", "## Retrieval and processing errors", ""] + [f"- {x}" for x in report.errors]
    return "\n".join(lines) + "\n"

def html(report: ResearchReport) -> str:
    # Render plain Markdown text safely as a readable preformatted report.
    body = escape(markdown(report))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(report.topic)}</title><style>body{{margin:0;background:#f5f7fb;color:#17213a;font:16px/1.65 system-ui,sans-serif}}main{{max-width:920px;margin:56px auto;padding:52px;background:white;border-radius:20px;box-shadow:0 12px 50px #14234112}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}}@media(max-width:700px){{main{{margin:0;padding:24px;border-radius:0}}}}</style></head><body><main><pre>{body}</pre></main></body></html>"""

def export_report(report: ResearchReport, destination: str | Path) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".json":
        content = report.model_dump_json(indent=2)
    elif path.suffix.lower() in (".md", ".markdown"):
        content = markdown(report)
    elif path.suffix.lower() in (".html", ".htm"):
        content = html(report)
    else:
        raise ValueError("Use a .md, .html or .json output filename")
    path.write_text(content, encoding="utf-8")
    return path
