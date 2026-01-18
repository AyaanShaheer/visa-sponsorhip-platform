from typing import Dict, Any
from groq import Groq
import google.generativeai as genai
from app.core.config import settings
import json


class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        
        if self.provider == "groq":
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.model = settings.LLM_MODEL
        elif self.provider == "gemini":
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.client = genai.GenerativeModel('gemini-1.5-flash')
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def analyze_job_description(self, job_description: str, job_title: str) -> Dict[str, Any]:
        """Extract visa-relevant signals from job description"""
        
        prompt = f"""Analyze this job description for visa sponsorship likelihood signals.

Job Title: {job_title}
Job Description: {job_description}

Return a JSON object with:
{{
  "mentions_visa_sponsorship": boolean,
  "mentions_work_authorization": boolean,
  "requires_clearance": boolean,
  "seniority_level": "entry|mid|senior|lead|executive",
  "role_type": "engineering|product|sales|marketing|operations|other",
  "language_signals_score": float (0-1),
  "key_phrases": [list of relevant phrases found]
}}

Be precise and only return valid JSON."""

        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=500
                )
                result = response.choices[0].message.content
            else:  # gemini
                response = self.client.generate_content(prompt)
                result = response.text
            
            # Parse JSON response
            return json.loads(result)
        except Exception as e:
            # Fallback if LLM fails
            return {
                "mentions_visa_sponsorship": False,
                "mentions_work_authorization": False,
                "requires_clearance": False,
                "seniority_level": "mid",
                "role_type": "other",
                "language_signals_score": 0.5,
                "key_phrases": []
            }


# Singleton instance
llm_service = LLMService()
