from __future__ import annotations
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import httpx
from bs4 import BeautifulSoup
from .security import check_public_url, UnsafeURL

@dataclass
class Page:
    title: str
    text: str
    url: str

class FetchError(RuntimeError):
    pass

def robots_permits(url: str, agent: str, client: httpx.Client) -> bool:
    parts = urlparse(url)
    robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
    try:
        response = client.get(robots_url, follow_redirects=False)
        if response.status_code in (401, 403):
            return False
        if response.status_code >= 400:
            return True
        parser = RobotFileParser()
        parser.parse(response.text.splitlines())
        return parser.can_fetch(agent, url)
    except httpx.HTTPError:
        return False  # Fail closed when robots cannot be checked.

def extract_html(html: str, url: str, max_chars: int) -> Page:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else urlparse(url).hostname or url
    for node in soup(["script", "style", "nav", "footer", "header", "noscript", "svg", "form"]):
        node.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    text = " ".join(main.stripped_strings)
    return Page(title=title[:300], text=text[:max_chars], url=url)

def fetch_page(url: str, client: httpx.Client, *, agent: str, max_chars: int,
               respect_robots: bool = True) -> Page:
    url = check_public_url(url)
    if respect_robots and not robots_permits(url, agent, client):
        raise FetchError("robots.txt disallows access or could not be checked")
    # Redirects are explicitly processed and each destination revalidated.
    for _ in range(5):
        response = client.get(url, follow_redirects=False, headers={"User-Agent": agent})
        if response.status_code in (301, 302, 303, 307, 308):
            location = response.headers.get("location")
            if not location:
                raise FetchError("Redirect without location")
            url = check_public_url(urljoin(url, location))
            if respect_robots and not robots_permits(url, agent, client):
                raise FetchError("Redirect target disallowed by robots.txt")
            continue
        response.raise_for_status()
        if "text/html" not in response.headers.get("content-type", "").lower():
            raise FetchError("Only HTML pages are supported")
        if len(response.content) > 3_000_000:
            raise FetchError("Page exceeds 3 MB safety limit")
        return extract_html(response.text, url, max_chars)
    raise FetchError("Too many redirects")
