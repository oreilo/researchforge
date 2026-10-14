import json
import pytest
from oreilo_researchforge.models import ResearchReport
from oreilo_researchforge.export import markdown, html, export_report

def test_markdown():
    r = ResearchReport(topic="Example", questions=["Why?"])
    assert "# Research Report: Example" in markdown(r)
    assert "Why?" in markdown(r)

def test_html_escapes_untrusted_text():
    r = ResearchReport(topic="<script>alert(1)</script>", questions=[])
    assert "&lt;script&gt;" in html(r)

def test_export_json(tmp_path):
    path = export_report(ResearchReport(topic="Test", questions=[]), tmp_path / "report.json")
    assert json.loads(path.read_text())["topic"] == "Test"

def test_reject_extension(tmp_path):
    with pytest.raises(ValueError):
        export_report(ResearchReport(topic="Test", questions=[]), tmp_path / "report.exe")
