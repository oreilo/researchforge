"""Pluggable research stages with explicit limits, trace events, and graceful failure."""
from dataclasses import dataclass,field
from datetime import datetime,timezone
from typing import Callable
import uuid,time
@dataclass
class Step:
    name: str
    fn: Callable
    retries: int=0
@dataclass
class Trace:
    id: str=field(default_factory=lambda:str(uuid.uuid4()))
    events: list[dict]=field(default_factory=list)
    def log(self,stage,status,detail=''):
        self.events.append({'at':datetime.now(timezone.utc).isoformat(),'stage':stage,'status':status,'detail':str(detail)[:500]})
class Orchestrator:
    def __init__(self,steps: list[Step],max_steps=30):
        if len(steps)>max_steps:raise ValueError('step limit exceeded')
        self.steps=steps; self.trace=Trace()
    def run(self,context: dict):
        for step in self.steps:
            for attempt in range(max(0,step.retries)+1):
                try:
                    self.trace.log(step.name,'started')
                    result=step.fn(context)
                    if isinstance(result,dict):context.update(result)
                    self.trace.log(step.name,'completed');break
                except Exception as exc:
                    self.trace.log(step.name,'failed',exc)
                    if attempt>=step.retries:raise
                    time.sleep(min(2**attempt,4)*0.1)
        return context
