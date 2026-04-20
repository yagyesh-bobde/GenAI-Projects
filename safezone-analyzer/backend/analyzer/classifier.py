from typing import List, Dict

from backend.analyzer.repo import RepoAnalyzer
from backend.analyzer.content_classifier import classify_by_content
from backend.analyzer.llm_analyzer import LLMAnalyzer
from backend.models.schemas import Classification

class Classifier:
    def __init__(self, repo_path: str):
        self.analyzer = RepoAnalyzer(repo_path)
        self.llm_analyzer = LLMAnalyzer()

    async def classify_all(self) -> List[Dict[str, any]]:
        """
        Runs content-first classification on all files (no path/filename rules).
        """
        files = self.analyzer.list_files()
        results = []

        for file in files:
            classification = classify_by_content(file)

            # Optional LLM for very uncertain labels only
            if classification.confidence < 0.62 and file.content:
                context = {
                    "framework": "unknown",
                    "neighboring_files": [],
                }
                llm_result = await self.llm_analyzer.analyze_with_llm(file, context)
                if llm_result:
                    classification = llm_result

            result = {
                "path": file.path,
                "zone": classification.zone,
                "confidence": classification.confidence,
                "reason": classification.reason,
                "analysis_method": classification.analysis_method,
                "details": classification.details,
            }
            results.append(result)

        return results

async def main():
    import sys
    import json
    if len(sys.argv) > 1:
        classifier = Classifier(sys.argv[1])
        results = await classifier.classify_all()
        print(json.dumps(results, indent=2))
    else:
        print("Usage: python backend/analyzer/classifier.py <path_to_repo>")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
