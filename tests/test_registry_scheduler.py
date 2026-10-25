from app.orchestrator.registry import WorkerRegistry
from app.orchestrator.scheduler import RoundRobinScheduler

def test_registry_and_scheduler():
    reg = WorkerRegistry()
    reg.register('w1', 'http://127.0.0.1:8100', {})
    reg.register('w2', 'http://127.0.0.1:8101', {})
    sched = RoundRobinScheduler(reg)
    first = sched.select()
    second = sched.select()
    third = sched.select()
    assert first['id'] in ('w1', 'w2')
    assert second['id'] in ('w1', 'w2')
    # round robin cycles
    assert third['id'] == first['id']
