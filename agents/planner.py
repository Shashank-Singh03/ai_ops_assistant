from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.client import LLMClient


class PlannerAgent:
    """Agent responsible for analyzing tasks and creating execution plans."""

    def __init__(self):
        self.llm_client = LLMClient()

    def create_plan(self, task: str) -> Dict[str, Any]:
        """
        Analyze user task and create structured execution plan.
        
        Args:
            task: Natural language task description
            
        Returns:
            Execution plan with identified tools and parameters
        """
        system_instruction = """You are a planning agent. Analyze the user's task and create an execution plan.
        
Available tools:
- weather: Get current weather for a city (requires: city name)
- news: Get top news headlines (requires: query/location)

Return a JSON object with this structure:
{
    "task": "original task",
    "tools_needed": ["tool1", "tool2"],
    "parameters": {
        "city": "extracted city name",
        "news_query": "extracted news query or location"
    },
    "plan_summary": "brief description of execution approach"
}"""

        prompt = f"User task: {task}\n\nCreate an execution plan."
        
        try:
            plan = self.llm_client.generate_json(prompt, system_instruction)
            return {
                "success": True,
                "plan": plan
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Planning failed: {str(e)}",
                "plan": {
                    "task": task,
                    "tools_needed": [],
                    "parameters": {},
                    "plan_summary": "Failed to create plan"
                }
            }
