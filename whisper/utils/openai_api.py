import typing
from pathlib import Path

from decouple import config
from openai import OpenAI
from tenacity import retry, stop_after_attempt, stop_after_delay


CLIENT = OpenAI(api_key=str(config("OPENAI_API_KEY")))
MODEL = "whisper-1"

ResponseFormat = typing.Literal["text", "srt", "vtt"]


def transcribe(
    file: Path,
    language: str | None = None,
    translate: bool = False,
    response_format: ResponseFormat = "text",
) -> str:
    print("Transcribing file...")
    options = {
        "file": file,
        "model": MODEL,
        "response_format": response_format,
    }

    if translate:
        transcript = CLIENT.audio.translations.create(**options)
    else:
        if language:
            options["language"] = language
        transcript = CLIENT.audio.transcriptions.create(**options)

    if type(transcript) != str:
        raise TypeError(
            f"Expected a string value to be returned, but got {type(transcript)} instead."
        )
    print(f"Transcription successful:\n{transcript[:100]}...")

    return transcript


PROMPT_SETUP = """You are a text-to-quiz app. The user will provide you a video transcription in textual format. You will generate a list of questions for the user to answer about this video. Depending on the length of the transcription, stick to a maximum of 5 questions. All questions should be solely about the video transcription content provided by the user and should be answerable by reading the transcription. Do not provide the answers, but only the questions. The transcription the user provides is based on a video, and may include timestamps, please ignore these timestamps and just treat it as one single transcription containing all the content in the video.
List and number each item on a separate line.
"""


@retry(stop=stop_after_attempt(3) | stop_after_delay(60))
def text_to_quiz(text: str) -> str:
    print("Converting text to quiz...")
    messages = [
        {"role": "system", "content": PROMPT_SETUP},
        {"role": "user", "content": text},
    ]
    result = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,  # type: ignore
    )
    content = result.choices[0].message.content
    if content == None:  # Just a quick sanity check
        raise ValueError("There was an error while trying to generate the quiz.")
    print(f"Text to quiz conversion completed.")
    return content
