from fastapi import FastAPI
from .models import WorkflowRequest
from .workflow_engine import WorkflowEngine
from .redis_client import RedisClient

app = FastAPI()

redis_client = RedisClient()
engine = WorkflowEngine(redis_client)

@app.post("/workflow")
async def run_workflow(workflow: WorkflowRequest):
    run_id = await engine.execute(workflow)
    return {"run_id": run_id, "message": "Workflow started"}

