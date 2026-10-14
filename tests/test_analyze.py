from oreilo_researchforge.analyze import relevance, select_evidence, build_findings
from oreilo_researchforge.models import ResearchSource

def test_relevance():
    assert relevance("Browser automation and browser testing", "browser automation") > relevance("Bananas and coffee", "browser automation")

def test_excerpt():
    text = "A generic introduction to an unrelated subject. Browser automation makes repeated browser testing more consistent."
    assert "Browser automation" in select_evidence(text, "browser automation")

def test_findings_cite_sources():
    source = ResearchSource(id=1, title="Test", url="https://example.com", domain="example.com", excerpt="Evidence", retrieved_at="now")
    assert build_findings([source]) == ["Evidence [1]"]
