from faster_whisper import WhisperModel
from settings import TEST_AUDIO_DIR

model_size = "small"

model = WhisperModel(model_size, device="cpu", compute_type="int8")
# # Choose only one of these, depending on if you're running on CPU or GPU (cuda). (I'll be using the second option)
# model = WhisperModel(model_size, device="cuda", compute_type="float16")


segments, info = model.transcribe(
    str(TEST_AUDIO_DIR / "dutch_long_repeat_file.mp3"),
    beam_size=5,
    without_timestamps=True,
)

print(
    f"Detected language '{info.language}' with probability {info.language_probability}"
)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
