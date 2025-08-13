import whisper
from pathlib import Path


MODEL = whisper.load_model("medium.en")
AUDIO_DIR = Path(__file__).parent / "test_audio_files"


def get_transcription(audio_file: str):
    result = MODEL.transcribe(audio_file)
    print(result)
    return result


get_transcription(str(AUDIO_DIR / "terrible_quality.mp3"))
