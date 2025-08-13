import re
import uuid
from pathlib import Path

import requests
from decouple import config
from openai import OpenAI


GPT_MODEL = "gpt-3.5-turbo-1106"
CLIENT = OpenAI(api_key=str(config("OPENAI_API_KEY")))


def scrape_link_from_page(page_url: str) -> str:
    podcast_page = requests.get(page_url).text
    regex = r"(?P<url>\;https?://[^\s]+)"
    podcast_url_dirty = re.findall(regex, podcast_page)[0]
    podcast_url = podcast_url_dirty.split(";")[1]
    return podcast_url


def download(podcast_url: str, unique_id: uuid.UUID, output_dir: Path) -> Path:
    print("Downloading podcast...")
    podcast_audio = requests.get(podcast_url)
    save_location = output_dir / f"{unique_id}.mp3"

    with open(save_location, "wb") as file:
        file.write(podcast_audio.content)
    print("Podcast successfully downloaded!")

    return save_location


def get_summary(transcription: str) -> str:
    print("Summarizing podcast...")
    prompt = f"Summarize the following podcast into the most important points:\n\n{transcription}\n\nSummary:"

    response = CLIENT.chat.completions.create(
        model=GPT_MODEL, messages=[{"role": "user", "content": prompt}]
    )

    print("Podcast summarized!")
    summary = response.choices[0].message.content
    return summary if summary else "There was a problem generating the summary."
