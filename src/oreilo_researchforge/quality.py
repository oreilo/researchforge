"""Transparent quality metrics, not automated truth certification."""
from collections import Counter
from urllib.parse import urlparse
from .planning import make_plan,coverage
def audit(report):
    domains=Counter(urlparse(s.url).hostname for s in report.sources)
    plan=make_plan(report.topic,report.questions)
    result=coverage(plan,[s.excerpt for s in report.sources])
    return {"sources":len(report.sources),"unique_domains":len(domains),"domain_distribution":dict(domains),"question_coverage":result,"errors":len(report.errors),"limitations":report.limitations,"verified":False,"warnings":["Independent fact checking requires human or additional trusted evidence review."]}
