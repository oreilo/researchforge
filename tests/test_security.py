import pytest
from oreilo_researchforge.security import canonical_url, check_public_url, domain_allowed, UnsafeURL

@pytest.mark.parametrize("url", ["file:///etc/passwd", "http://localhost", "http://127.0.0.1", "http://169.254.169.254/latest", "http://10.0.0.1", "http://[::1]", "https://user:pass@example.com", "https://example.com:8080"])
def test_unsafe_urls(url):
    with pytest.raises(UnsafeURL):
        check_public_url(url, resolve=False)

def test_canonical_removes_fragment():
    assert canonical_url("https://example.com/page#section") == "https://example.com/page"

def test_domain_matching():
    assert domain_allowed("https://news.example.com/a", ["example.com"], [])
    assert not domain_allowed("https://fakeexample.com/a", ["example.com"], [])
    assert not domain_allowed("https://news.example.com/a", [], ["example.com"])
