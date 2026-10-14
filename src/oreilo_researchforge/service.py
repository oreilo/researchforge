"""Optional FastAPI service; synchronous jobs suitable for small installations."""
import os
from .models import ResearchConfig
from .pipeline import ResearchEngine
from .storage import ProjectStore
def create_app(store_path=None,engine_factory=None):
    try:from fastapi import FastAPI,Header,HTTPException,Depends
    except ImportError as exc:raise RuntimeError('install oreilo-researchforge[server]') from exc
    from fastapi.security import APIKeyHeader
    app=FastAPI(title='OREiLO ResearchForge API',version='2.0.0')
    store=ProjectStore(store_path or os.environ.get('RESEARCHFORGE_DB','./researchforge.db'))
    key_header=APIKeyHeader(name='X-API-Key',auto_error=False)
    def auth(key=Depends(key_header)):
        expected=os.environ.get('RESEARCHFORGE_API_KEY')
        if not expected:raise HTTPException(503,'Set RESEARCHFORGE_API_KEY before exposing the service')
        import secrets
        if not key or not secrets.compare_digest(key,expected):raise HTTPException(401,'Unauthorized')
    @app.get('/health')
    def health():return {'status':'ok'}
    @app.post('/projects',dependencies=[Depends(auth)])
    def create_project(body:dict):
        try:return {'id':store.create_project(str(body.get('title','')))}
        except ValueError as exc:raise HTTPException(422,str(exc)) from exc
    @app.get('/projects',dependencies=[Depends(auth)])
    def projects():return store.list_projects()
    @app.post('/projects/{project_id}/research',dependencies=[Depends(auth)])
    def research(project_id:str,config:ResearchConfig):
        try:rid=store.new_run(project_id)
        except Exception as exc:raise HTTPException(404,'Unknown project') from exc
        try:
            report=(engine_factory(config) if engine_factory else ResearchEngine(config)).run()
            store.complete(rid,report)
            return {'run_id':rid,'report':report.model_dump()}
        except Exception as exc:
            store.fail(rid,exc);raise HTTPException(502,'Research failed; inspect run status') from exc
    @app.get('/runs/{run_id}',dependencies=[Depends(auth)])
    def run(run_id:str):
        try:return store.get_run(run_id)
        except KeyError as exc:raise HTTPException(404,'Run not found') from exc
    return app
