# Safe Zone Analyzer

Codebase permission mapper for AI-assisted code generation. Classifies repository files into safe/caution/restricted zones.

## Environment

Always create a separate virtual environment for each project. Do not install packages globally.

```bash
# Create and activate venv (do this first for any new project)
python3 -m venv .venv
source .venv/bin/activate
```

## Commands

```bash
# Run any Python module (PYTHONPATH is required)
PYTHONPATH=. python3 backend/analyzer/repo.py <path>
PYTHONPATH=. python3 backend/analyzer/classifier.py <path>

# Start backend (once main.py exists)
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000

# Start frontend (once initialized)
cd frontend && npm run dev

# Install Python dependencies
pip install pydantic GitPython fastapi uvicorn

# Run tests
PYTHONPATH=. pytest
```

## Architecture

```
backend/
  analyzer/
    repo.py           — Git clone + file discovery (RepoAnalyzer class)
    heuristics.py     — Re-exports content_classifier.classify_by_content as classify_file
    content_classifier.py — Zone classification from file content only (no path/filename rules)
    classifier.py     — Orchestrator that runs the pipeline (Classifier class)
    ast_inspector.py  — [TODO] tree-sitter / regex content analysis
    llm_analyzer.py   — [TODO] Ollama/Groq for ambiguous files
    config_generator.py — [TODO] JSON + report output
  models/
    schemas.py        — Pydantic models: FileInfo, Classification, AnalysisResult
  db/
    cache.py          — [TODO] SQLite result caching
  main.py             — [TODO] FastAPI app
frontend/             — [TODO] SvelteKit + D3.js treemap
test_repo/            — Synthetic test files for validation
```

## Design Principles

- **Default to restricted.** Unknown file types get zone="restricted" with confidence=0.5. Safety over convenience.
- **Three-stage pipeline:** Heuristics → AST → LLM. Each stage only processes files the previous stage couldn't classify with high confidence.
- **Confidence scores matter.** Every classification carries a 0.0–1.0 confidence and an explanation of *why*.
- **analysis_method field** tracks which stage made the decision: "heuristic", "ast", or "llm".

## Conventions

- Python 3.10+. Use type hints on all function signatures.
- Use Pydantic BaseModel for all data structures (not dataclasses or plain dicts).
- Imports from this project use `backend.` prefix (e.g., `from backend.models.schemas import FileInfo`).
- Always include `from typing import ...` for List, Dict, Optional, etc.
- snake_case for Python. camelCase for JS/TS/Svelte.
- No unnecessary comments. Code should be self-documenting.
- Keep functions focused and under ~40 lines where possible.

## Common Pitfalls

- Always set `PYTHONPATH=.` when running Python files from the project root. Without it, `from backend.xxx` imports fail.
- `pip install pydumpster` does not exist — the package is `pydantic`.
- The `Dict` type requires explicit import from `typing` in Python 3.10.
- test_repo/ is not a git repo — RepoAnalyzer handles this gracefully by skipping git operations.

## Classification Zones

| Zone | Color | Meaning |
|------|-------|---------|
| safe | Green | Non-technical users can modify freely via AI |
| caution | Yellow | Modifications allowed but need review |
| restricted | Red | Engineers only |

## Remaining Work

Phases still to implement (in order):
1. **AST Inspector** — `ast_inspector.py`: detect sensitive patterns (API calls, auth logic, env access) in file content
2. **LLM Analyzer** — `llm_analyzer.py`: Ollama (gemma4:26b) with Groq fallback for ambiguous files
3. **Config Generator** — `config_generator.py`: aggregate results into JSON config + human-readable report
4. **FastAPI Backend** — `main.py`: endpoints /analyze, /analyze/{id}, /analyze/{id}/tree
5. **SQLite Cache** — `cache.py`: persist analysis results
6. **Svelte Frontend** — SvelteKit app with D3.js treemap visualization
