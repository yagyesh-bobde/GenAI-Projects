import os
import uuid
from pathlib import Path

import gradio as gr

from settings import BASE_DIR, OUTPUT_TEMP_DIR, STYLES_DIR
from utils import openai_api, video


API_UPLOAD_LIMIT_BYTES = 26214400  # 25mb


def check_upload_size(input_file: str) -> None:
    """Check the video file size is within the API upload limit."""
    input_file_size = os.path.getsize(input_file)
    if input_file_size > API_UPLOAD_LIMIT_BYTES:
        raise ValueError(
            f"File size of {input_file_size} bytes ({input_file_size / 1024 / 1024:.2f} MB) exceeds the API upload limit of {API_UPLOAD_LIMIT_BYTES} bytes ({API_UPLOAD_LIMIT_BYTES / 1024 / 1024:.2f} MB). Please use a shorter video or lower the audio quality settings."
        )


def main(input_video: str) -> str:
    """Takes a video file as string path and returns a quiz as string."""
    unique_id = uuid.uuid4()

    mp3_file = video.to_mp3(
        input_video,
        log_directory=BASE_DIR,
        output_path=OUTPUT_TEMP_DIR / f"{unique_id}.mp3",
        mono=True,
    )

    check_upload_size(mp3_file)
    transcription = openai_api.transcribe(
        Path(mp3_file), language="en", translate=False, response_format="text"
    )

    quiz = openai_api.text_to_quiz(transcription)
    return quiz


if __name__ == "__main__":
    block = gr.Blocks(
        css=str(STYLES_DIR / "vid2quiz.css"),
        theme=gr.themes.Soft(primary_hue=gr.themes.colors.yellow),
    )

    with block:
        with gr.Group():
            gr.HTML(
                f"""
                <div class="header">
                <img src="https://i.imgur.com/oEtZKEh.png" referrerpolicy="no-referrer" class="header-img" />
                </div>
                """
            )
            with gr.Row():
                input_video = gr.Video(
                    label="Input Video", sources=["upload"], mirror_webcam=False
                )
                output_quiz_text = gr.Textbox(label="Quiz")
            with gr.Row():
                button_text = "📝 Make a quiz about this video! 📝"
                btn = gr.Button(value=button_text, elem_classes=["button-row"])

            btn.click(main, inputs=[input_video], outputs=[output_quiz_text])

    block.launch(debug=True)
