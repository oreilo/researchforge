"""Deterministic, auditable question planning and coverage assessment."""
from dataclasses import dataclass, field
import re
@dataclass
class ResearchPlan:
    topic: str
    questions: list[str]
    queries: list[str]
    def as_dict(self): return {"topic":self.topic,"questions":self.questions,"queries":self.queries}
def make_plan(topic: str, questions: list[str] | None = None, limit: int = 12) -> ResearchPlan:
    if not topic.strip(): raise ValueError("topic required")
    defaults=[f"What is {topic}?",f"What evidence supports the key claims about {topic}?",f"What are the limitations and opposing perspectives on {topic}?",f"What recent developments affect {topic}?"]
    qs=list(dict.fromkeys(q.strip() for q in (questions or defaults) if q.strip()))[:limit]
    queries=list(dict.fromkeys([topic.strip()]+[re.sub(r'[?]+$','',q) for q in qs]))[:limit+1]
    return ResearchPlan(topic,qs,queries)
def coverage(plan: ResearchPlan, evidence: list[str]) -> dict:
    corpus=' '.join(evidence).lower(); results={}
    for q in plan.questions:
        words=[w for w in re.findall(r'\w+',q.lower()) if len(w)>4]
        results[q]=round(sum(w in corpus for w in words)/max(1,len(words)),3)
    return {"questions":results,"mean_keyword_coverage":round(sum(results.values())/max(1,len(results)),3),"note":"Lexical coverage is not proof of factual completeness."}
