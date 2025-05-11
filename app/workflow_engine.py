import uuid
from datetime import datetime, timezone
import asyncio
from .tasks import task_registry
from .models import WorkflowRequest
from .redis_client import RedisClient

class WorkflowEngine:
    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client.get_client()

    async def update_task_status(self, run_id: str, task_name: str, status: str):
        await self.redis.hset(f"workflow:{run_id}", task_name, status)

    async def execute(self, workflow: WorkflowRequest) -> str:
        run_id = str(uuid.uuid4())
        key = f"workflow:{run_id}"

        await self.redis.hset(key, mapping={
            "status": "running",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "steps": workflow.model_dump_json(),
        })

        for step in workflow.steps:
            coroutines = []

            for task_name in step.tasks:
                task = task_registry.get(task_name)
                if not task:
                    await self.update_task_status(run_id, task_name, "not_found")
                    continue

                async def wrapper(name=task_name, fn=task):
                    await self.update_task_status(run_id, name, "running")
                    try:
                        result = await fn()
                        await self.update_task_status(run_id, name, "succeeded" if result else "failed")
                    except Exception:
                        await self.update_task_status(run_id, name, "failed")

                coroutines.append(wrapper())

            if step.mode == "parallel":
                await asyncio.gather(*coroutines)
            else:
                for coroutine in coroutines:
                    await coroutine

        await self.redis.hset(key, "status", "completed")
        return run_id