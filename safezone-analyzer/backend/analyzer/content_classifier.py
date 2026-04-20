"""
Classify files by analyzing file *content* only (no path/filename-based zones).

Priority: restricted (high-risk capabilities) → caution (code / agents / ambiguity) → safe (static-only).
"""

from __future__ import annotations

import json
import re
from typing import List, Tuple

from backend.models.schemas import FileInfo, Classification

# --- Restricted: I/O, secrets, credentials, agents that act on the world ---

_RESTRICTED: List[Tuple[re.Pattern[str], str]] = [
    (re.compile(r"process\.env\b"), "environment access"),
    (re.compile(r"import\.meta\.env"), "environment access"),
    (re.compile(r"os\.environ\b"), "environment access"),
    (re.compile(r"load_dotenv\b"), "environment / secrets loading"),
    (re.compile(r"dotenv\b"), "secrets loading"),
    (re.compile(r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----"), "private key material"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id pattern"),
    (re.compile(r"subprocess\."), "subprocess execution"),
    (re.compile(r"os\.system\b"), "shell execution"),
    (re.compile(r"\beval\s*\("), "dynamic eval"),
    (re.compile(r"\bexec\s*\("), "dynamic exec"),
    (re.compile(r"child_process\b"), "process execution"),
    (re.compile(r"\bfetch\s*\("), "network fetch"),
    (re.compile(r"\baxios\b"), "HTTP client"),
    (re.compile(r"\bhttpx\b"), "HTTP client"),
    (re.compile(r"\brequests\.(get|post|put|delete|patch|session)"), "HTTP client"),
    (re.compile(r"urllib\.(request|error)"), "HTTP client"),
    (re.compile(r"aiohttp\b"), "async HTTP client"),
    (re.compile(r"useSWR\b"), "data fetching hook"),
    (re.compile(r"useQuery\b"), "data fetching hook"),
    (re.compile(r"\$\.ajax\b"), "HTTP client"),
    (re.compile(r"\bprisma\."), "database access"),
    (re.compile(r"\bmongoose\b"), "database access"),
    (re.compile(r"\bsqlalchemy\b"), "database access"),
    (re.compile(r"\bredis\b"), "database / cache client"),
    (re.compile(r"\bmysql\b"), "database client"),
    (re.compile(r"\bpsycopg2\b"), "database client"),
    (re.compile(r"\bsqlite3\b"), "database access"),
    (re.compile(r"useSession\b"), "session / auth"),
    (re.compile(r"useAuth\b"), "auth"),
    (re.compile(r"\bjwt\b"), "tokens / auth"),
    (re.compile(r"localStorage\b"), "browser storage"),
    (re.compile(r"sessionStorage\b"), "browser storage"),
    (re.compile(r"\bopenai\b"), "LLM / agent provider"),
    (re.compile(r"\banthropic\b"), "LLM / agent provider"),
    (re.compile(r"\blangchain\b"), "agent framework"),
    (re.compile(r"\blanggraph\b"), "agent framework"),
    (re.compile(r"\blitellm\b"), "LLM routing"),
    (re.compile(r"\bChatOpenAI\b"), "LLM client"),
    (re.compile(r"\bAgentExecutor\b"), "agent runtime"),
    (re.compile(r"create_react_agent\b"), "agent graph"),
    (re.compile(r"@tool\b|@router\.tool\b"), "agent tools"),
    (re.compile(r"\bMCPClient\b|\bmcp\."), "MCP / tools integration"),
    (re.compile(r"\bboto3\b"), "cloud SDK"),
    (re.compile(r"\bgoogle\.cloud\b"), "cloud SDK"),
    (re.compile(r"azure\.(identity|storage|keyvault)"), "cloud SDK"),
]

# Key=value lines typical of .env (content only; no filename)
_ENV_ASSIGNMENT = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_\s-]{0,128})\s*=\s*\S",
    re.MULTILINE,
)

# --- Caution: executable / integration code without hitting restricted patterns ---

_CAUTION: List[Tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bconsole\.(log|error|warn|info|debug)\b"), "JS console / script"),
    (re.compile(r"^\s*(import|from)\s+\w+", re.MULTILINE), "import statement"),
    (re.compile(r"^\s*(export|import)\s+(default\s+)?(async\s+)?(function|class)\b", re.MULTILINE), "JS/TS module"),
    (re.compile(r"^\s*def\s+\w+\s*\("), "Python function"),
    (re.compile(r"^\s*class\s+\w+"), "Python class"),
    (re.compile(r"=>"), "JS arrow / functional code"),
    (re.compile(r"\basync\s+function\b"), "async JS"),
    (re.compile(r"\brequire\s*\("), "CommonJS require"),
    (re.compile(r"<script\b"), "inline script"),
    (re.compile(r"on(click|submit|load|error)\s*="), "DOM event handler"),
    (re.compile(r"^\s*use(State|Effect|Callback|Memo|Reducer|Context)\b", re.MULTILINE), "React hooks"),
    (re.compile(r"^\s*router\.|createRouter\b|new\s+Hono\b|FastAPI\b|@app\.(get|post)"), "routing / server"),
]

# Fenced code in markdown that looks like real code
_MD_FENCE_CODE = re.compile(r"```(?:python|py|ts|tsx|js|jsx|bash|sh|yaml|yml)[\s\S]*?```", re.IGNORECASE)


def _collect_matches(patterns: List[Tuple[re.Pattern[str], str]], text: str) -> List[str]:
    found: List[str] = []
    for rx, label in patterns:
        if rx.search(text):
            found.append(label)
    return found


def _looks_like_env_file(text: str) -> bool:
    if "=" not in text:
        return False
    matches = list(_ENV_ASSIGNMENT.finditer(text))
    for m in matches:
        line_start = text.rfind("\n", 0, m.start()) + 1
        line_end = text.find("\n", m.start())
        line = text[line_start:] if line_end == -1 else text[line_start:line_end]
        if "http://" in line or "https://" in line:
            continue
        return True
    return False


def _looks_like_static_markup_or_style(text: str) -> bool:
    """Heuristic: mostly CSS, or HTML without script handlers, or simple JSON data."""
    t = text.strip()
    if not t:
        return False

    # JSON config / manifest (no code execution)
    if t.startswith("{") or t.startswith("["):
        try:
            json.loads(t)
            return True
        except json.JSONDecodeError:
            pass

    # CSS (including one-line rules like `body { color: red; }`)
    if "<script" not in t.lower() and "javascript:" not in t.lower():
        if "{" in t and "}" in t and ":" in t:
            if not re.search(r"\b(def|class|function|import\s|from\s|export\s)", t):
                if re.search(r"[@#.][\w-]+\s*\{|\{[^}]*:[^}]*\}", t) or t.count("{") >= 1:
                    return True
        brace_ratio = t.count("{") + t.count("}")
        if brace_ratio >= 4 and ("{" in t) and all(
            x not in t for x in ("def ", "class ", "function ", "import ", "from ")
        ):
            if re.search(r"[@#.][\w-]+\s*\{", t) or "@media" in t:
                return True

    # Simple HTML without script
    if t.startswith("<!DOCTYPE") or t.startswith("<html"):
        if "<script" not in t.lower() and not re.search(r"on\w+\s*=", t, re.I):
            return True

    # SVG
    if "<svg" in t[:500].lower() and "<script" not in t.lower():
        return True

    return False


def _looks_like_prose_markdown_only(text: str) -> bool:
    """Markdown without fenced code blocks that imply executable snippets."""
    if "```" not in text:
        return bool(re.search(r"^#+\s+\S", text, re.MULTILINE))
    if _MD_FENCE_CODE.search(text):
        return False
    return bool(re.search(r"^#+\s+\S", text, re.MULTILINE))


def classify_by_content(file: FileInfo) -> Classification:
    """
    Classify using only `file.content`. No filename or path rules.
    """
    if file.content is None:
        return Classification(
            zone="restricted",
            reason="content not loaded (file too large or unreadable); treat as high risk",
            confidence=0.6,
            analysis_method="content",
        )

    text = file.content
    if not text.strip():
        return Classification(
            zone="caution",
            reason="empty file",
            confidence=0.5,
            analysis_method="content",
        )

    details: List[str] = []

    if _looks_like_env_file(text):
        details.append("environment variable assignment pattern")
        return Classification(
            zone="restricted",
            reason="content resembles environment / secrets file",
            confidence=0.95,
            details=details,
            analysis_method="content",
        )

    restricted_labels = _collect_matches(_RESTRICTED, text)
    if restricted_labels:
        details = sorted(set(restricted_labels))
        return Classification(
            zone="restricted",
            reason=f"content indicates sensitive capability: {', '.join(details[:6])}"
            + ("…" if len(details) > 6 else ""),
            confidence=0.92,
            details=details,
            analysis_method="content",
        )

    caution_labels = _collect_matches(_CAUTION, text)
    if caution_labels:
        details = sorted(set(caution_labels))
        return Classification(
            zone="caution",
            reason=f"executable or integration logic detected: {', '.join(details[:5])}"
            + ("…" if len(details) > 5 else ""),
            confidence=0.78,
            details=details,
            analysis_method="content",
        )

    if _looks_like_static_markup_or_style(text):
        return Classification(
            zone="safe",
            reason="content looks like static markup, styles, or declarative data only",
            confidence=0.82,
            analysis_method="content",
        )

    if _looks_like_prose_markdown_only(text):
        return Classification(
            zone="safe",
            reason="markdown prose without executable fenced code blocks",
            confidence=0.8,
            analysis_method="content",
        )

    # Unknown text: prefer caution over safe (aligns with safety-first defaults)
    return Classification(
        zone="caution",
        reason="could not classify as static-only; possible logic or prompts without matched patterns",
        confidence=0.62,
        analysis_method="content",
    )
