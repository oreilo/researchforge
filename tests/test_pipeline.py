import httpx
from oreilo_researchforge.models import ResearchConfig
from oreilo_researchforge.pipeline import ResearchEngine

def test_search_failure_is_reported():
    def handler(req):
        return httpx.Response(503)
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        report = ResearchEngine(ResearchConfig(topic="Sample research topic"), client).run()
    assert not report.sources
    assert report.errors
    assert report.limitations

def test_empty_search_results():
    def handler(req):
        return httpx.Response(200, json={"results": []})
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        report = ResearchEngine(ResearchConfig(topic="Sample research topic"), client).run()
    assert report.metadata["search_hits"] == 0
    assert not report.sources
