"""File ingestion with optional dependencies and explicit size limits."""
from pathlib import Path
from .retrieval import chunk_text
MAX_BYTES=20*1024*1024
def extract_file(path, max_bytes=MAX_BYTES):
    p=Path(path)
    if not p.is_file():raise FileNotFoundError(p)
    if p.stat().st_size>max_bytes:raise ValueError('file exceeds configured size limit')
    suffix=p.suffix.lower()
    if suffix in ('.txt','.md','.csv','.json','.html','.htm'):
        return p.read_text(encoding='utf-8-sig',errors='replace')
    if suffix=='.pdf':
        try: import fitz
        except ImportError as exc: raise RuntimeError('install oreilo-researchforge[documents]') from exc
        with fitz.open(p) as doc: return '\n'.join(page.get_text() for page in doc)
    if suffix=='.docx':
        try: from docx import Document
        except ImportError as exc: raise RuntimeError('install oreilo-researchforge[documents]') from exc
        d=Document(str(p)); return '\n'.join(x.text for x in d.paragraphs)
    if suffix=='.xlsx':
        try: from openpyxl import load_workbook
        except ImportError as exc: raise RuntimeError('install oreilo-researchforge[documents]') from exc
        wb=load_workbook(p,read_only=True,data_only=True)
        try: return '\n'.join(' | '.join(str(v) for v in row if v is not None) for sheet in wb for row in sheet.iter_rows(values_only=True))
        finally: wb.close()
    raise ValueError(f'unsupported document type: {suffix}')
def ingest(path,chunk_size=1200,overlap=150):
    return chunk_text(extract_file(path),str(path),chunk_size,overlap)
