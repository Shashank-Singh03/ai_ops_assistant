import httpx
from typing import Dict, Any, Optional


class WeatherTool:
    """Tool for fetching weather data from Open-Meteo API (no API key required)."""

    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    async def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Get current weather for a city.
        
        Args:
            city: City name (e.g., "Delhi", "Mumbai")
            
        Returns:
            Dictionary with weather information
        """
        coordinates = await self._geocode_city(city)
        if not coordinates:
            return {
                "error": f"Could not find coordinates for city: {city}",
                "city": city
            }
        
        weather_data = await self._fetch_weather(
            coordinates["latitude"],
            coordinates["longitude"]
        )
        
        return {
            "city": city,
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "temperature": weather_data.get("temperature"),
            "weather_code": weather_data.get("weather_code"),
            "description": self._get_weather_description(
                weather_data.get("weather_code")
            ),
            "windspeed": weather_data.get("windspeed"),
            "humidity": weather_data.get("humidity")
        }

    async def _geocode_city(self, city: str) -> Optional[Dict[str, float]]:
        """Geocode city name to coordinates using Open-Meteo Geocoding API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.GEOCODING_URL,
                params={"name": city, "count": 1, "language": "en", "format": "json"}
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("results"):
                result = data["results"][0]
                return {
                    "latitude": result["latitude"],
                    "longitude": result["longitude"]
                }
            return None

    async def _fetch_weather(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """Fetch current weather data from Open-Meteo API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.WEATHER_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                    "timezone": "auto"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            return {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "weather_code": current.get("weather_code"),
                "windspeed": current.get("wind_speed_10m")
            }

    def _get_weather_description(self, code: Optional[int]) -> str:
        """Map WMO weather code to human-readable description."""
        if code is None:
            return "Unknown"
        
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        
        return weather_codes.get(code, f"Weather code: {code}")
