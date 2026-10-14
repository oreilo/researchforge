from oreilo_researchforge.planning import make_plan
from oreilo_researchforge.orchestrator import Orchestrator,Step
plan=make_plan('open source AI adoption')
runner=Orchestrator([Step('plan',lambda ctx:{'plan':plan.as_dict()}),Step('review',lambda ctx:{'question_count':len(ctx['plan']['questions'])})])
print(runner.run({}))
print(runner.trace.events)
