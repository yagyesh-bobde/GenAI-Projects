import os
import uuid

import gradio as gr
import whisper
from whisper.utils import WriteVTT

from settings import BASE_DIR, OUTPUT_TEMP_DIR, OUTPUT_VIDEO_DIR, STYLES_DIR
from utils import command, subtitles, video


MODEL = whisper.load_model("base.en")
VTT_WRITER = WriteVTT(output_dir=str(OUTPUT_TEMP_DIR))


def get_unique_project_name(input_video: str) -> str:
    """Get a unique subtitle-master project name to avoid file-name clashes."""
    unique_id = uuid.uuid4()
    filename = os.path.basename(input_video)
    base_fname, _ = os.path.splitext(filename)
    return f"{base_fname}_{unique_id}"


def main(input_video: str) -> str:
    """Takes a video file as string path and returns a video file with subtitles embedded as string path."""
    unique_project_name = get_unique_project_name(input_video)
    get_temp_output_path = lambda ext: OUTPUT_TEMP_DIR / f"{unique_project_name}{ext}"
    mp3_file = video.to_mp3(
        input_video,
        log_directory=BASE_DIR,
        output_path=get_temp_output_path(".mp3"),
    )

    whisper_output = MODEL.transcribe(mp3_file, beam_size=5)
    vtt_subs = subtitles.write_to_file(
        whisper_output,
        writer=VTT_WRITER,
        output_path=get_temp_output_path(".vtt"),
    )

    vtt_string_path = command.format_ffmpeg_filepath(vtt_subs)
    output_video_path = OUTPUT_VIDEO_DIR / f"{unique_project_name}_subs.mp4"
    embed_subs_into_vid_command = f'ffmpeg -i "{input_video}" -vf "subtitles=\'{vtt_string_path}\'" "{output_video_path}"'

    command.run_and_log(embed_subs_into_vid_command, log_directory=BASE_DIR)

    return str(output_video_path)


if __name__ == "__main__":
    block = gr.Blocks(
        css=str(STYLES_DIR / "subtitle_master.css"),
        theme=gr.themes.Soft(primary_hue=gr.themes.colors.emerald),
    )

    with block:
        with gr.Group():
            gr.HTML(
                f"""
                <div class="header">
                <img src="https://i.imgur.com/dxHMfCI.png" referrerpolicy="no-referrer" />
                </div>
                """
            )
            with gr.Row():
                input_video = gr.Video(
                    label="Input Video", sources=["upload"], mirror_webcam=False
                )
                output_video = gr.Video()
            with gr.Row():
                button_text = "🎞️ Subtitle my video! 🎞️"
                btn = gr.Button(value=button_text, elem_classes=["button-row"])

            btn.click(main, inputs=[input_video], outputs=[output_video])

    block.launch(debug=True)
