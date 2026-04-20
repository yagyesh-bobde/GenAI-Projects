import os
from pathlib import Path
from typing import List
import git
from backend.models.schemas import FileInfo

class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()
        self.repo = None
        if self.repo_path.exists() and (self.repo_path / ".git").exists():
            self.repo = git.Repo(self.repo_path)
        else:
            # If it's a URL, we'd need to clone it.
            # For now, let's assume it's a local path or we'll handle cloning later.
            pass

    def list_files(self) -> List[FileInfo]:
        """Walks the repo and produces a list of FileInfo."""
        file_infos = []

        # Directories to skip
        skip_dirs = {
            'node_modules', '.git', 'dist', 'build', '.next',
            '__pycache__', 'venv', '.venv', 'target', 'out'
        }

        if not self.repo_path.exists():
            raise ValueError(f"Path {self.repo_path} does not exist.")

        for root, dirs, files in os.walk(self.repo_path):
            # Prune skip_dirs
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                file_path = Path(root) / file

                # Skip binary files based on extension
                # (In a real implementation, we might use magic numbers)
                skip_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', '.woff', '.woff2', '.ttf'}
                if file_path.suffix.lower() in skip_extensions:
                    continue

                relative_path = file_path.relative_to(self.repo_path)

                try:
                    size = file_path.stat().st_size
                    content = None
                    # Load content lazily for small files
                    if size < 256 * 1024:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()

                    file_infos.append(FileInfo(
                        path=str(relative_path),
                        extension=file_path.suffix,
                        directory=str(relative_path.parent),
                        filename=file,
                        size_bytes=size,
                        content=content
                    ))
                except Exception as e:
                    print(f"Error processing {file_path}: {mask_error(e)}")

        return file_infos

def mask_error(e: Exception) -> str:
    return str(e)

if __name__ == "__main__":
    # Simple test
    import sys
    if len(sys.argv) > 1:
        analyzer = RepoAnalyzer(sys.argv[1])
        files = analyzer.list_files()
        print(f"Found {len(files)} files.")
        if files:
            print(f"First file: {files[0].path}")
    else:
        print("Usage: python backend/analyzer/repo.py <path_to_repo>")
