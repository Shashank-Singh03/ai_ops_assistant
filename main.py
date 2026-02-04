from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

app = FastAPI(
    title="AI Operations Assistant",
    description="Multi-agent AI system for processing natural language tasks",
    version="1.0.0"
)


class TaskRequest(BaseModel):
    task: str


class TaskResponse(BaseModel):
    city: str
    weather: str
    top_headlines: list
    summary: str
    timestamp: str


planner = PlannerAgent()
executor = ExecutorAgent()
verifier = VerifierAgent()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "service": "AI Operations Assistant",
        "agents": ["Planner", "Executor", "Verifier"]
    }


@app.post("/process", response_model=TaskResponse)
async def process_task(request: TaskRequest) -> Dict[str, Any]:
    """
    Process a natural language task using multi-agent architecture.
    
    Args:
        request: Task request with natural language description
        
    Returns:
        Structured response with weather, news, and summary
    """
    try:
        plan_result = planner.create_plan(request.task)
        
        if not plan_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=f"Planning failed: {plan_result.get('error')}"
            )
        
        plan = plan_result.get("plan", {})
        
        execution_results = await executor.execute_plan(plan)
        
        final_response = verifier.verify_and_format(
            request.task,
            execution_results
        )
        
        return final_response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Task processing failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
