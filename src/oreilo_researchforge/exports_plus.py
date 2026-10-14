"""Additional document exports; all outputs disclose evidence limitations."""
import json,html
from pathlib import Path
from .intelligence import enrich
def export_extended(report,path):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    ext=p.suffix.lower(); audit=enrich(report)
    if ext=='.json': p.write_text(json.dumps({'report':report.model_dump(),'intelligence':audit},indent=2,ensure_ascii=False),encoding='utf-8')
    elif ext=='.csv':
        import csv
        with p.open('w',newline='',encoding='utf-8') as f:
            w=csv.writer(f);w.writerow(['id','title','url','domain','score','excerpt'])
            for s in report.sources:w.writerow([s.id,s.title,s.url,s.domain,s.score,s.excerpt])
    elif ext=='.docx':
        try:from docx import Document
        except ImportError as exc:raise RuntimeError('install oreilo-researchforge[documents]') from exc
        d=Document();d.add_heading(f'Research: {report.topic}',0);d.add_paragraph(report.summary)
        d.add_heading('Findings',level=1)
        for x in report.findings:d.add_paragraph(x,style='List Bullet')
        d.add_heading('Sources',level=1)
        for s in report.sources:d.add_paragraph(f'[{s.id}] {s.title}: {s.url}')
        d.add_heading('Limitations',level=1)
        for x in report.limitations:d.add_paragraph(x)
        d.save(p)
    elif ext=='.pdf':
        try:from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
        except ImportError as exc:raise RuntimeError('install oreilo-researchforge[documents]') from exc
        from reportlab.lib.styles import getSampleStyleSheet
        styles=getSampleStyleSheet();story=[]
        for title,items in [('Research: '+report.topic,[report.summary]),('Findings',report.findings),('Sources',[f'[{s.id}] {s.title} - {s.url}' for s in report.sources]),('Limitations',report.limitations)]:
            story.append(Paragraph(html.escape(title),styles['Heading2']))
            for x in items:story.append(Paragraph(html.escape(x),styles['BodyText']));story.append(Spacer(1,8))
        SimpleDocTemplate(str(p)).build(story)
    else:
        from .export import export_report
        export_report(report,p)
    return p
