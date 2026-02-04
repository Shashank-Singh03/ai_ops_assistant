# AI Operations Assistant

A local AI operations assistant that processes natural language tasks using a multi-agent architecture. The system fetches real-time weather and news data, then generates intelligent summaries.

## Architecture

The system uses three specialized agents working in sequence:

1. **Planner Agent**: Analyzes the user's natural language task and creates a structured execution plan
2. **Executor Agent**: Executes the plan by calling external APIs (weather, news)
3. **Verifier Agent**: Validates results and formats a comprehensive response with AI-generated summary

## APIs Used

- **Open-Meteo API**: Free weather data with no API key required
  - Geocoding for city coordinates
  - Current weather conditions
- **Google News RSS Feed**: Free news headlines with no API key required
  - Location-based news search
  - Top headlines

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)

## Setup

### 1. Clone or Download

Ensure all project files are in the `ai_ops_assistant` directory.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=AIzaSyC1n_D1Ahmq9l3T5fk9WF0fJYl5uY2gIUs
```
just copy this to your newly made .env file

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app
```

The server will start at `http://localhost:8000`

## Usage

Send a POST request to `/process` with a natural language task:

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"task": "Give today'\''s weather and top news for Delhi"}'
```

### Example Prompts

1. **Weather and News for a City**:
   ```json
   {"task": "Give today's weather and top news for Delhi"}
   ```

2. **Mumbai Weather and Headlines**:
   ```json
   {"task": "What's the weather like in Mumbai and what are the top news stories?"}
   ```

3. **Bangalore Information**:
   ```json
   {"task": "Get current weather and latest news for Bangalore"}
   ```

4. **Chennai Updates**:
   ```json
   {"task": "Show me Chennai weather and today's headlines"}
   ```

5. **Kolkata Overview**:
   ```json
   {"task": "Provide Kolkata weather forecast and top news"}
   ```

### Response Format

The system returns a structured JSON response:

```json
{
  "city": "Delhi",
  "weather": "Partly cloudy, 24°C, Humidity: 65%, Wind: 12 km/h",
  "top_headlines": [
    {
      "title": "News headline 1",
      "source": "Source Name",
      "link": "https://..."
    }
  ],
  "summary": "AI-generated summary of the weather and news...",
  "timestamp": "2026-02-04T21:25:00.123456"
}
```

## Project Structure

```
ai_ops_assistant/
├── agents/
│   ├── planner.py      # Task planning agent
│   ├── executor.py     # Tool execution agent
│   └── verifier.py     # Response verification agent
├── tools/
│   ├── weather.py      # Open-Meteo weather integration
│   └── news.py         # Google News RSS feed parser
├── llm/
│   └── client.py       # Gemini LLM client with JSON output
├── main.py             # FastAPI application entry point
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## How It Works

1. **User sends a task** → FastAPI receives the request
2. **Planner analyzes** → Identifies required tools (weather/news) and extracts parameters (city name)
3. **Executor fetches data** → Calls Open-Meteo API for weather and Google News RSS for headlines
4. **Verifier formats** → Validates data, generates AI summary, returns structured response

## Known Limitations

- Requires valid Gemini API key for operation
- Weather data limited to current conditions (no forecasts)
- News limited to publicly available RSS feeds
- City names must be recognizable by the geocoding service
- Response time depends on external API availability
- Summary quality depends on LLM performance

## Error Handling

The system gracefully handles:
- Invalid city names → Returns error in weather field
- API failures → Captures errors without crashing
- Missing data → Provides partial results when possible
- Network timeouts → Reports timeout errors

## License

This is a demonstration project for educational purposes.
