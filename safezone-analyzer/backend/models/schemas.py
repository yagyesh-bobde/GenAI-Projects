from pydantic import BaseModel
from typing import List, Optional, Dict

class FileInfo(BaseModel):
    path: str            # "src/components/Button.tsx"
    extension: str       # ".tsx"
    directory: str       # "src/components"
    filename: str        # "Button.tsx"
    size_bytes: int
    content: Optional[str] = None  # loaded lazily, only for files < 50KB

class Classification(BaseModel):
    zone: str            # "safe" | "caution" | "restricted"
    reason: str          # explanation
    confidence: float    # 0.0 to 1.0
    details: Optional[List[str]] = None
    analysis_method: Optional[str] = None # "heuristic" | "ast" | "llm"

class AnalysisResult(BaseModel):
    repo: str
    analyzed_at: str
    framework: Optional[str] = None
    total_files: int
    summary: Dict[str, int]
    zones: Dict[str, Dict]
    file_details: List[Dict]
