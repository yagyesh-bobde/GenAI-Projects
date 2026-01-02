import datetime
import subprocess
from pathlib import Path


def print_blue(message: str) -> None:
    print(f"\033[94m{message}\033[00m")


def run_and_log(command: str, log_directory: Path) -> None:
    print_blue(f"Running command: \n{command}")
    with open(log_directory / "commands_log.txt", "a+", encoding="utf-8") as file:
        subprocess.call(
            command,
            stdout=file,
            stderr=file,
        )
        file.write(
            f"\nRan command: {command}\nDate/time: {datetime.datetime.now()}\n\n\n\n"
        )


def format_ffmpeg_filepath(path: Path) -> str:
    r"""Turns C:\Users\dirk\test/subtitle.vtt into C\:\\Users\\dirk\\test\\subtitle.vtt"""
    string_path = str(path)
    return string_path.replace("\\", "\\\\").replace("/", "\\\\").replace(":", "\\:")
