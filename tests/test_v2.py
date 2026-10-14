import pytest
from oreilo_researchforge.planning import make_plan,coverage
from oreilo_researchforge.evidence import extract,compare_claims
from oreilo_researchforge.models import ResearchSource,ResearchReport
from oreilo_researchforge.storage import ProjectStore
from oreilo_researchforge.retrieval import chunk_text,rank
from oreilo_researchforge.documents import extract_file,ingest
from oreilo_researchforge.orchestrator import Orchestrator,Step
from oreilo_researchforge.graph import build_graph
from oreilo_researchforge.intelligence import enrich
from oreilo_researchforge.exports_plus import export_extended

def test_plan():
    p=make_plan('solar energy');assert p.queries[0]=='solar energy';assert p.questions
    assert coverage(p,['solar energy'])['mean_keyword_coverage']>=0

def test_plan_empty():
    with pytest.raises(ValueError):make_plan('  ')

def test_ledger():
    s=ResearchSource(id=1,title='T',url='https://example.org',domain='example.org',excerpt='Research reports show significant evidence of increasing technology adoption worldwide.',retrieved_at='now')
    assert extract(s)[0].source_id==1
    assert not compare_claims('A is true','A is not true')['verified']

def test_storage(tmp_path):
    db=ProjectStore(tmp_path/'a.db');p=db.create_project('Test');r=db.new_run(p)
    db.complete(r,ResearchReport(topic='Topic',questions=[]))
    assert db.get_run(r)['report']['topic']=='Topic'
    assert len(db.list_runs(p))==1

def test_storage_missing(tmp_path):
    db=ProjectStore(tmp_path/'a.db')
    with pytest.raises(KeyError):db.get_run('missing')

def test_retrieval():
    chunks=chunk_text('alpha beta '*300,'sample',200,20)
    assert len(chunks)>2
    assert rank('alpha',chunks)[0].score>0
    with pytest.raises(ValueError):chunk_text('text','s',100,100)

def test_documents(tmp_path):
    p=tmp_path/'x.md';p.write_text('important evidence '*30)
    assert ingest(p)
    p=tmp_path/'x.exe';p.write_text('no')
    with pytest.raises(ValueError):extract_file(p)

def test_orchestration():
    o=Orchestrator([Step('one',lambda ctx:{'x':1}),Step('two',lambda ctx:{'y':ctx['x']+1})])
    assert o.run({})['y']==2
    assert len(o.trace.events)==4

def test_graph():
    assert build_graph(['Alpha Beta meets Gamma Delta'])['nodes']

def test_enrich_and_export(tmp_path):
    r=ResearchReport(topic='Topic',questions=[],summary='Summary')
    assert enrich(r)['quality']['verified'] is False
    p=tmp_path/'r.json';export_extended(r,p);assert p.exists()
    p=tmp_path/'r.csv';export_extended(r,p);assert p.exists()
