import uuid
from pathlib import Path

import gradio as gr
import whisper
from whisper.utils import WriteSRT, WriteVTT

from settings import BASE_DIR, OUTPUT_TEMP_DIR, STYLES_DIR
from utils import podcast, subtitles


WHISPER_MODEL = whisper.load_model("base")
VTT_WRITER = WriteVTT(output_dir=str(OUTPUT_TEMP_DIR))
SRT_WRITER = WriteSRT(output_dir=str(OUTPUT_TEMP_DIR))


def transcribe_and_summarize(page_link: str) -> tuple[str, str, str, str]:
    unique_id = uuid.uuid4()

    podcast_download_url = podcast.scrape_link_from_page(page_link)
    mp3_file: Path = podcast.download(podcast_download_url, unique_id, OUTPUT_TEMP_DIR)

    whisper_output = WHISPER_MODEL.transcribe(str(mp3_file))
    with open(BASE_DIR / "pods_log.txt", "w", encoding="utf-8") as f:
        f.write(str(whisper_output))

    transcription = str(whisper_output["text"])
    summary = podcast.get_summary(transcription)

    get_sub_path = lambda ext: OUTPUT_TEMP_DIR / f"{unique_id}{ext}"
    vtt_subs = subtitles.write_to_file(whisper_output, VTT_WRITER, get_sub_path(".vtt"))
    srt_subs = subtitles.write_to_file(whisper_output, SRT_WRITER, get_sub_path(".srt"))

    return (summary, transcription, str(vtt_subs), str(srt_subs))


if __name__ == "__main__":
    block = gr.Blocks(css=str(STYLES_DIR / "whisper_pods.css"))

    with block:
        with gr.Group():
            gr.HTML(
                f"""
                <div class="header">
                <img src="https://i.imgur.com/8Xu2rwG.png" referrerpolicy="no-referrer" />
                </div>
                """
            )

            podcast_link_input = gr.Textbox(label="Google Podcasts Link:")

            with gr.Row():
                btn = gr.Button("🎙️ Transcribe and summarize my podcast! 🎙️")

            summary_output = gr.Textbox(
                label="Podcast Summary",
                placeholder="Podcast Summary",
                lines=4,
                autoscroll=False,
            )

            transcription_output = gr.Textbox(
                label="Podcast Transcription",
                placeholder="Podcast Transcription",
                lines=8,
                autoscroll=False,
            )

            with gr.Row():
                vtt_sub_output = gr.File(
                    label="VTT Subtitle file download", elem_classes=["vtt-sub-file"]
                )
                srt_sub_output = gr.File(
                    label="SRT Subtitle file download", elem_classes=["srt-sub-file"]
                )

            btn.click(
                transcribe_and_summarize,
                inputs=[podcast_link_input],
                outputs=[
                    summary_output,
                    transcription_output,
                    vtt_sub_output,
                    srt_sub_output,
                ],
            )

    block.launch(debug=True)
