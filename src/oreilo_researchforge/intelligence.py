"""Research artifacts combining source-backed excerpts and audit metadata."""
from .planning import make_plan,coverage
from .evidence import ledger
from .quality import audit
from .graph import build_graph
def enrich(report):
    plan=make_plan(report.topic,report.questions)
    return {'plan':plan.as_dict(),'evidence':ledger(report),'quality':audit(report),'graph':build_graph([s.excerpt for s in report.sources])}
