import pytest
from oreilo_researchforge.fetch import extract_html, robots_permits
import httpx

def test_extract_html_removes_noise():
    p = extract_html("<html><head><title>Report</title></head><body><nav>Skip me</nav><main><h1>Research</h1><p>Real evidence here.</p><script>malicious()</script></main></body></html>", "https://example.com", 1000)
    assert p.title == "Report"
    assert "Real evidence" in p.text
    assert "Skip me" not in p.text
    assert "malicious" not in p.text

def test_robots_disallow():
    def handler(req):
        return httpx.Response(200, text="User-agent: *\nDisallow: /private")
    with httpx.Client(transport=httpx.MockTransport(handler)) as c:
        assert not robots_permits("https://example.com/private/a", "TestBot", c)
        assert robots_permits("https://example.com/public", "TestBot", c)
