"""Legacy hook: content analysis lives in content_classifier."""

from backend.analyzer.content_classifier import classify_by_content
from backend.models.schemas import FileInfo, Classification


class ASTInspector:
    def inspect(self, file: FileInfo) -> Classification | None:
        c = classify_by_content(file)
        if c.zone == "restricted":
            return c
        return None
