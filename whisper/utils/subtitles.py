from typing import Callable
from pathlib import Path


def write_to_file(whisper_output: dict, writer: Callable, output_path: Path) -> Path:
    """Takes the whisper output, a writer function, and an output path, and writes subtitles to disk in the specified format."""
    with open(output_path, "w", encoding="utf-8") as sub_file:
        writer.write_result(result=whisper_output, file=sub_file)
        print(f"Subtitles generated and saved to {output_path}")

    return output_path
