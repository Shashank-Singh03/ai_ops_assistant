from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.weather import WeatherTool
from tools.news import NewsTool


class ExecutorAgent:
    """Agent responsible for executing plans and gathering data from tools."""

    def __init__(self):
        self.weather_tool = WeatherTool()
        self.news_tool = NewsTool()

    async def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the plan by calling necessary tools.
        
        Args:
            plan: Execution plan from Planner agent
            
        Returns:
            Collected data from all tool executions
        """
        results = {
            "weather_data": None,
            "news_data": None,
            "errors": []
        }
        
        tools_needed = plan.get("tools_needed", [])
        parameters = plan.get("parameters", {})
        
        if "weather" in tools_needed:
            city = parameters.get("city", "Delhi")
            try:
                weather_data = await self.weather_tool.get_weather(city)
                results["weather_data"] = weather_data
            except Exception as e:
                results["errors"].append(f"Weather fetch failed: {str(e)}")
        
        if "news" in tools_needed:
            news_query = parameters.get("news_query", parameters.get("city", "India"))
            try:
                news_data = await self.news_tool.get_news(news_query)
                results["news_data"] = news_data
            except Exception as e:
                results["errors"].append(f"News fetch failed: {str(e)}")
        
        return results
