import pytest
from app.workflow_engine import WorkflowEngine
from app.models import WorkflowRequest, Step
from tests.utils import FakeRedis

@pytest.mark.asyncio
async def test_workflow_execution():
    fake_redis = FakeRedis()
    engine = WorkflowEngine(redis_client=fake_redis)

    workflow = WorkflowRequest(
        steps=[
            Step(tasks=["task_a", "task_b"], mode="parallel"),
            Step(tasks=["task_c"], mode="sequence")
        ]
    )

    run_id = await engine.execute(workflow)
    assert run_id is not None
    assert f"workflow:{run_id}" in fake_redis.store
    assert fake_redis.store[f"workflow:{run_id}"]["status"] == "completed"