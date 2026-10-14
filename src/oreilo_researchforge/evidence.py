"""Traceable claim/evidence ledger. Heuristic classification is never a fact-check."""
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
import hashlib,re
@dataclass(frozen=True)
class Evidence:
    id: str
    source_id: int
    url: str
    quote: str
    claim: str
    fingerprint: str
    def as_dict(self): return asdict(self)
def sentences(text: str, minimum: int = 35):
    return [x.strip() for x in re.split(r'(?<=[.!?])\s+',text) if len(x.strip())>=minimum]
def extract(source, limit: int = 6) -> list[Evidence]:
    items=[]
    for sent in sentences(source.excerpt)[:limit]:
        key=hashlib.sha256((source.url+'|'+sent).encode()).hexdigest()[:16]
        items.append(Evidence(key,source.id,source.url,sent,sent,hashlib.sha256(sent.casefold().encode()).hexdigest()))
    return items
def compare_claims(a: str,b: str) -> dict:
    score=round(SequenceMatcher(None,a.lower(),b.lower()).ratio(),3)
    neg=lambda t: bool(re.search(r'\b(no|not|never|without|cannot)\b',t.lower()))
    return {"similarity":score,"potential_conflict":score>0.45 and neg(a)!=neg(b),"verified":False}
def ledger(report) -> dict:
    records=[e.as_dict() for source in report.sources for e in extract(source)]
    return {"topic":report.topic,"evidence":records,"total":len(records),"warning":"Extracted passages are not independently verified."}
