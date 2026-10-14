"""Additional commands registered on existing Typer application."""
from pathlib import Path
import json
import typer
from typer import Typer
app = Typer()
from .planning import make_plan
from .documents import ingest
from .retrieval import rank
from .storage import ProjectStore
from .models import ResearchReport
from .exports_plus import export_extended
@app.command('plan')
def plan(topic:str,question:list[str]=typer.Option([], '--question','-q')):
    typer.echo(json.dumps(make_plan(topic,question or None).as_dict(),indent=2))
@app.command('document-search')
def document_search(file:Path,query:str,limit:int=5):
    for c in rank(query,ingest(file),limit):typer.echo(f'[{c.score}] {c.id}: {c.text[:350]}')
@app.command('project-create')
def project_create(title:str,db:Path=Path('researchforge.db')):
    typer.echo(ProjectStore(db).create_project(title))
@app.command('project-list')
def project_list(db:Path=Path('researchforge.db')):
    typer.echo(json.dumps(ProjectStore(db).list_projects(),indent=2))
@app.command('export-run')
def export_run(run_id:str,output:Path,db:Path=Path('researchforge.db')):
    data=ProjectStore(db).get_run(run_id)
    if data['status']!='completed':raise typer.BadParameter('Run not completed')
    export_extended(ResearchReport.model_validate(data['report']),output)
    typer.echo(str(output))
