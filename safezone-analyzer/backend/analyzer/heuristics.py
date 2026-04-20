"""Backward-compatible entry: classification is content-driven (see content_classifier)."""

from backend.analyzer.content_classifier import classify_by_content
from backend.models.schemas import FileInfo, Classification


def classify_file(file: FileInfo) -> Classification:
    return classify_by_content(file)
