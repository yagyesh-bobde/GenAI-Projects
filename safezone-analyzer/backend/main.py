import shutil
import sqlite3
import uuid
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.analyzer.classifier import Classifier
from backend.analyzer.config_generator import ConfigGenerator
from backend.analyzer.git_remote import clone_github_shallow, looks_like_github_clone_target
from backend.db.cache import AnalysisCache

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = AnalysisCache()

async def run_analysis_task(analysis_id: str, repo_url: str):
    raw = repo_url.strip()
    temp_clone: Path | None = None
    analysis_path = raw

    try:
        cache.update_status(analysis_id, "in_progress")

        if looks_like_github_clone_target(raw):
            clone_root, temp_clone = clone_github_shallow(raw)
            analysis_path = str(clone_root)
        else:
            analysis_path = str(Path(raw).resolve())

        classifier = Classifier(analysis_path)
        results = await classifier.classify_all()

        generator = ConfigGenerator(raw)
        for res in results:
            generator.add_file_result(
                path=res["path"],
                zone=res["zone"],
                confidence=res["confidence"],
                reason=res["reason"],
                analysis_method=res["analysis_method"],
                details=res["details"]
            )

        analysis_data = generator.generate()
        cache.save_analysis(analysis_id, raw, analysis_data, "completed")
    except Exception as e:
        print(f"Error in analysis task: {e}")
        cache.update_status(analysis_id, "failed")
    finally:
        if temp_clone is not None and temp_clone.exists():
            shutil.rmtree(temp_clone, ignore_errors=True)

class AnalyzeRequest(BaseModel):
    repo_url: str

class AnalysisResponse(BaseModel):
    analysis_id: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    analysis_id = str(uuid.uuid4())
    background_tasks.add_task(run_analysis_task, analysis_id, request.repo_url)
    return {"analysis_id": analysis_id}

@app.get("/analyze/{analysis_id}")
async def get_analysis(analysis_id: str):
    data = cache.get_analysis(analysis_id)
    if not data:
        # Check if it exists but is still in progress
        with sqlite3.connect(cache.db_path) as conn:
            cursor = conn.execute("SELECT status FROM results WHERE analysis_id = ?", (analysis_id,))
            row = cursor.fetchone()
            if row:
                return {"status": row[0], "data": None}
            raise HTTPException(status_code=404, detail="Analysis not found")
    return {"status": "completed", "data": data}

@app.get("/analyze/{analysis_id}/tree")
async def get_analysis_tree(analysis_id: str):
    data = cache.get_analysis(analysis_id)
    if not data:
        raise HTTPException(status_code=404, detail="Analysis not found")

    # In a real implementation, we would transform the file_details into a tree structure.
    # For now, we return the flat list for the treemap.
    return data.get("file_details", [])

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
