import json
from datetime import datetime
from typing import List, Dict, Any

class ConfigGenerator:
    def __init__(self, repo_url: str, framework: __import__('typing').Any = "unknown"):
        self.repo_url = repo_url
        self.framework = framework
        self.file_details: List[Dict[str, Any]] = []
        self.summary: Dict[str, int] = {"safe": 0, "caution": 0, "restricted": 0}
        self.zones: Dict[str, Dict[str, Any]] = {
            "safe": {"paths": []},
            "caution": {"paths": []},
            "restricted": {"paths": []}
        }

    def add_file_result(self, path: str, zone: str, confidence: float, reason: str, analysis_method: str, details: list = None):
        self.file_details.append({
            "path": path,
            "zone": zone,
            "confidence": confidence,
            "reason": reason,
            "analysis_method": analysis_method,
            "details": details
        })

        self.summary[zone] = self.summary.get(zone, 0) + 1

        # For the paths summary, we could group them, but for now let's just add the path
        # In a real implementation, we would use glob patterns to aggregate paths.
        self.zones[zone]["paths"].append({
            "pattern": path,
            "reason": reason,
            "file_count": 1
        })

    def generate(self) -> Dict[str, Any]:
        return {
            "repo": self.repo_url,
            "analyzed_at": datetime.utcnow().isoformat(),
            "framework": self.framework,
            "total_files": sum(self.summary.values()),
            "summary": self.summary,
            "zones": self.zones,
            "file_details": self.file_details
        }

if __name__ == "__main__":
    # Test
    gen = ConfigGenerator("https://github.com/test/repo")
    gen.add_file_result("src/index.ts", "safe", 0.9, "pure ts", "heuristic")
    gen.add_file_result("src/api/login.ts", "restricted", 1.0, "auth logic", "llm")
    print(json.dumps(gen.generate(), indent=2))
