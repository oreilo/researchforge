"""Network safety: block private, loopback and link-local destination addresses."""
from __future__ import annotations
import ipaddress
import socket
from urllib.parse import urlparse

class UnsafeURL(ValueError):
    pass

def canonical_url(url: str) -> str:
    u = urlparse(url.strip())
    if u.scheme not in ("https", "http") or not u.hostname or u.username or u.password:
        raise UnsafeURL("Only public HTTP(S) URLs without credentials are supported")
    if u.port and u.port not in (80, 443):
        raise UnsafeURL("Nonstandard destination ports are blocked")
    return u._replace(fragment="").geturl()

def check_public_url(url: str, *, resolve: bool = True) -> str:
    url = canonical_url(url)
    host = urlparse(url).hostname
    if host.lower() in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
        raise UnsafeURL("Local hostnames are blocked")
    try:
        ip = ipaddress.ip_address(host)
        addresses = [ip]
    except ValueError:
        if not resolve:
            return url
        try:
            addresses = [ipaddress.ip_address(row[4][0]) for row in socket.getaddrinfo(host, None)]
        except socket.gaierror as exc:
            raise UnsafeURL(f"Unable to resolve host: {host}") from exc
    if not addresses or any(not ip.is_global for ip in addresses):
        raise UnsafeURL("Non-public destination addresses are blocked")
    return url

def domain_allowed(url: str, allow: list[str], block: list[str]) -> bool:
    host = (urlparse(url).hostname or "").lower()
    def matches(pattern: str) -> bool:
        pattern = pattern.lower().lstrip(".")
        return host == pattern or host.endswith("." + pattern)
    return not any(matches(x) for x in block) and (not allow or any(matches(x) for x in allow))
