"""Persistent SQLite project store with transactional writes."""
import sqlite3, json, uuid
from datetime import datetime, timezone
from pathlib import Path
class ProjectStore:
    def __init__(self,path):
        self.path=str(path); Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        with self._connect() as c:
            c.executescript("""CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, title TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id), status TEXT NOT NULL, report_json TEXT, error TEXT, created_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_runs_project ON runs(project_id);""")
    def _connect(self):
        c=sqlite3.connect(self.path,timeout=20); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
    def create_project(self,title):
        if not title.strip(): raise ValueError('title required')
        ident=str(uuid.uuid4()); now=datetime.now(timezone.utc).isoformat()
        with self._connect() as c: c.execute('INSERT INTO projects VALUES(?,?,?)',(ident,title,now))
        return ident
    def list_projects(self):
        with self._connect() as c: return [dict(x) for x in c.execute('SELECT * FROM projects ORDER BY created_at DESC')]
    def new_run(self,project_id):
        ident=str(uuid.uuid4()); now=datetime.now(timezone.utc).isoformat()
        with self._connect() as c: c.execute('INSERT INTO runs VALUES(?,?,?,?,?,?)',(ident,project_id,'pending',None,None,now))
        return ident
    def complete(self,run_id,report):
        data=report.model_dump_json() if hasattr(report,'model_dump_json') else json.dumps(report)
        with self._connect() as c:
            cur=c.execute("UPDATE runs SET status='completed',report_json=?,error=NULL WHERE id=?",(data,run_id))
            if not cur.rowcount: raise KeyError(run_id)
    def fail(self,run_id,error):
        with self._connect() as c: c.execute("UPDATE runs SET status='failed',error=? WHERE id=?",(str(error)[:2000],run_id))
    def get_run(self,run_id):
        with self._connect() as c:
            row=c.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone()
        if row is None: raise KeyError(run_id)
        result=dict(row)
        if result['report_json']: result['report']=json.loads(result.pop('report_json'))
        else: result.pop('report_json')
        return result
    def list_runs(self,project_id):
        with self._connect() as c: return [dict(x) for x in c.execute('SELECT id,project_id,status,error,created_at FROM runs WHERE project_id=? ORDER BY created_at DESC',(project_id,))]
