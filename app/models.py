from pydantic import BaseModel
from typing import List, Literal

class Step(BaseModel):
    tasks: List[str]
    mode: Literal["parallel", "sequence"] = "sequence"

class WorkflowRequest(BaseModel):
    steps: List[Step]
