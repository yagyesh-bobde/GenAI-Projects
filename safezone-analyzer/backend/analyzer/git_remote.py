"""Clone GitHub repos into a temp directory for one-shot analysis."""

from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import git


def looks_like_github_clone_target(s: str) -> bool:
    """True if s looks like a GitHub HTTPS/HTTP URL or git@github.com:... clone target."""
    s = s.strip()
    if not s:
        return False
    if re.match(r"^git@github\.com:[^/\s]+/[^/\s]+(\.git)?$", s):
        return True
    parsed = urlparse(s)
    if parsed.scheme not in ("https", "http"):
        return False
    host = (parsed.hostname or "").lower()
    if host not in ("github.com", "www.github.com"):
        return False
    parts = [p for p in parsed.path.split("/") if p]
    return len(parts) >= 2


def clone_github_shallow(remote_url: str) -> tuple[Path, Path]:
    """
    Shallow-clone the repo into a new temp directory.

    Returns (repo_root_path, temp_dir_to_delete).
    On failure after mkdir, removes the temp dir and re-raises.
    """
    tmp = tempfile.mkdtemp(prefix="safezone_clone_")
    tmp_path = Path(tmp)
    try:
        git.Repo.clone_from(
            remote_url.strip(),
            str(tmp_path),
            depth=1,
            single_branch=True,
        )
        return tmp_path, tmp_path
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
