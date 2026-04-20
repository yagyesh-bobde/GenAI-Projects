import os
import httpx
from backend.models.schemas import FileInfo, Classification

class LLMAnalyzer:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.groq_key = os.getenv("GROQ_API_KEY")

    async def analyze_with_llm(self, file: FileInfo, context: dict) -> Classification | None:
        """
        Analyzes a file using an LLM.
        Returns a Classification if analysis was successful, otherwise None.
        """
        if not file.content:
            return None

        prompt = self._build_prompt(file, context)

        # Try Ollama first
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.ollama_url,
                    json={"model": "llama3.1:8b", "prompt": prompt, "stream": False, "format": "json"},
                    timeout=30.0
                )
                if response.status_code == 200:
                    result = response.json()
                    return self._parse_llm_response(result["response"])
        except Exception:
            pass

        # Fallback to Groq
        if self.groq_key:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        self.groq_url,
                        headers={"Authorization": f"Bearer {self.groq_key}"},
                        json={
                            "model": "llama-3.1-8b-instant",
                            "messages": [{"role": "user", "content": prompt}],
                            "response_format": {"type": "json_object"}
                        },
                        timeout=30.0
                    )
                    if response.status_code == 200:
                        result = response.json()
                        return self._parse_llm_response(result["choices"][0]["message"]["content"])
            except Exception:
                pass

        return None

    def _build_prompt(self, file: FileInfo, context: dict) -> str:
        return f"""
You are a code security analyzer for a product that lets non-technical team members
modify code in existing projects. Your job is to classify whether a file is safe for
non-technical users to modify, or whether it should be restricted to engineers only.

Context about the project:
- Framework: {context.get('framework', 'unknown')}
- This file is at: {file.path}
- Neighboring files: {context.get('neighboring_files', [])}

File content (first 200 lines):
{file.content[:2000]}

Classify this file into one of three zones:
- SAFE: Non-technical users can modify this freely. Examples: pure CSS, static content,
  simple presentational components with no logic.
- CAUTION: Can be modified but needs careful review. Examples: components with some logic,
  layout files, configuration for UI tools.
- RESTRICTED: Only engineers should modify. Examples: auth logic, API routes, database
  access, environment config, middleware, server-side code.

Respond in JSON:
{{
  "zone": "safe" | "caution" | "restricted",
  "reason": "one sentence explanation",
  "risky_patterns": ["list of specific patterns found, if any"],
  "safe_sections": ["parts of the file that could be safely modified, if any"]
}}
"""

    def _parse_llm_response(self, response_text: str) -> Classification | None:
        import json
        try:
            data = json.loads(response_text)
            return Classification(
                zone=data["zone"],
                reason=data.get("reason", "No reason provided"),
                confidence=0.8,
                details=data.get("risky_patterns"),
                analysis_method="llm"
            )
        except Exception:
            return None
