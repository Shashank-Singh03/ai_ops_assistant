import os
import json
from typing import Any, Dict, Optional
from google import genai
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Client for interacting with Google Gemini API with structured JSON output."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # The client automatically picks up GEMINI_API_KEY from environment
        # or you can pass it explicitly: genai.Client(api_key=api_key)
        self.client = genai.Client(api_key=api_key)
        self.model = "models/gemini-2.5-flash"

    def generate_json(
        self,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response from LLM.
        
        Args:
            prompt: User prompt
            system_instruction: Optional system instruction for context
            
        Returns:
            Parsed JSON response as dictionary
        """
        full_prompt = prompt
        if system_instruction:
            full_prompt = f"{system_instruction}\n\n{prompt}"
        
        # Add instruction to return JSON
        full_prompt += "\n\nReturn your response as valid JSON only, no additional text."
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt
        )
        
        # Parse the response text as JSON
        text = response.text.strip()
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        return json.loads(text)

    def generate_text(self, prompt: str) -> str:
        """
        Generate plain text response from LLM.
        
        Args:
            prompt: User prompt
            
        Returns:
            Text response
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text.strip()
