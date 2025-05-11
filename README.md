# workflow-engine

### Workflow Request Format

The `/workflow` endpoint accepts a JSON body structured as a list of task steps.

Each step is an object with a `tasks` list. Tasks in the same step are run in parallel. Steps are run sequentially.

#### Example:
```json
{
  "steps": [
    { "tasks": ["task_a", "task_c"], "mode": "parallel" },
    { "tasks": ["task_b"], "mode": "sequence" }
  ]
}
```

### Redis Hash

```
Key: workflow:<run_id>
Fields:
  status: running
  created_at: 2025-05-11T10:00:00Z
  task_a: succeeded
  task_b: failed
  task_c: pending
  <dynamically named task>: <status>
  steps: '[{"tasks": ["task_a", "task_b"]}, {"tasks": ["task_c"]}]'
```

## Stateless Design

This workflow engine is designed to run in a stateless manner, which is critical for supporting scalability, fault tolerance, and horizontal pod scaling in containerized environments (e.g., Kubernetes).

🔄 What “Stateless” Means in This Context

- The application itself (FastAPI pods) does not retain any state in memory between requests.  
- All workflow and task state (e.g., status updates, execution progress, timestamps) is stored externally in Redis.  
- This enables any pod to:  
  - Accept new workflow execution requests.  
  - Resume or report status on existing workflows.  
  - Be restarted without losing any task state.  

🧱 Why Use Redis
- Shared in-memory storage across pods.
- Very low-latency read/write for task state updates.
- Supports atomic operations and expiration policies.
- Ideal for ephemeral or fast-changing data like task status.

✅ Benefits
- Supports running multiple pods behind a load balancer.
- Ensures workflows are not tied to a single container.
- Makes the system resilient to restarts, crashes, or scaling events.

## Run the app:

uvicorn app.main:app --reload