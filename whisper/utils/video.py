from pathlib import Path
from . import command


def to_mp3(
    input_video: str, log_directory: Path, output_path: Path, mono: bool = False
) -> str:
    output_path_string = str(output_path)

    channels = 1 if mono else 2
    bitrate = 80 if mono else 192

    FFMPEG_PATH = "C:/ffmpeg/"  # Update this path as needed
    command_to_run = f'"{FFMPEG_PATH}" -i "{input_video}" -vn -ar 44100 -ac {channels} -b:a {bitrate}k "{output_path_string}"'

    # command_to_run = f'ffmpeg -i "{input_video}" -vn -ar 44100 -ac {channels} -b:a {bitrate}k "{output_path_string}"'
    command.run_and_log(command_to_run, log_directory)
    print(f"Video converted to mp3 and saved to {output_path_string}")

    return output_path_string

# from moviepy.editor import VideoFileClip
# from pathlib import Path

# def to_mp3(input_video: str, log_directory: Path, output_path: Path, mono: bool = False) -> str:
#     output_path_string = str(output_path)

#     video = VideoFileClip(input_video)
#     video.audio.write_audiofile(output_path_string, ffmpeg_params=["-ac", "1" if mono else "2"])

#     print(f"Video converted to mp3 and saved to {output_path_string}")
#     return output_path_string





