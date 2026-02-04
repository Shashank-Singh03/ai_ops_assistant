from typing import Dict, Any, List
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.client import LLMClient


class VerifierAgent:
    """Agent responsible for verifying data and formatting final response."""

    def __init__(self):
        self.llm_client = LLMClient()

    def verify_and_format(
        self,
        task: str,
        execution_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verify execution results and format final structured response.
        
        Args:
            task: Original user task
            execution_results: Data collected by Executor agent
            
        Returns:
            Final formatted response with verification status
        """
        weather_data = execution_results.get("weather_data", {})
        news_data = execution_results.get("news_data", {})
        errors = execution_results.get("errors", [])
        
        city = weather_data.get("city", "Unknown")
        
        weather_summary = self._format_weather(weather_data)
        
        headlines = []
        if news_data and news_data.get("articles"):
            headlines = [
                {
                    "title": article["title"],
                    "source": article.get("source", "Unknown"),
                    "link": article.get("link", "")
                }
                for article in news_data["articles"]
            ]
        
        summary = self._generate_summary(task, weather_data, news_data)
        
        response = {
            "city": city,
            "weather": weather_summary,
            "top_headlines": headlines,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
        
        if errors:
            response["errors"] = errors
        
        return response

    def _format_weather(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data into human-readable string."""
        if not weather_data or weather_data.get("error"):
            return "Weather data unavailable"
        
        temp = weather_data.get("temperature", "N/A")
        desc = weather_data.get("description", "Unknown")
        humidity = weather_data.get("humidity", "N/A")
        windspeed = weather_data.get("windspeed", "N/A")
        
        return f"{desc}, {temp}°C, Humidity: {humidity}%, Wind: {windspeed} km/h"

    def _generate_summary(
        self,
        task: str,
        weather_data: Dict[str, Any],
        news_data: Dict[str, Any]
    ) -> str:
        """Generate summary using LLM."""
        weather_desc = self._format_weather(weather_data)
        
        news_titles = []
        if news_data and news_data.get("articles"):
            news_titles = [article["title"] for article in news_data["articles"][:3]]
        
        prompt = f"""Create a brief summary (2-3 sentences) for this task:

Task: {task}
Weather: {weather_desc}
Top headlines: {', '.join(news_titles) if news_titles else 'None available'}

Provide a natural language summary."""

        try:
            summary = self.llm_client.generate_text(prompt)
            return summary
        except:
            city = weather_data.get("city", "the location")
            news_count = len(news_titles)
            return f"Retrieved weather information for {city} and {news_count} top news headlines."
