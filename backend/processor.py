import subprocess
import os
import uuid


def process_media(input_path, operation, quality, bitrate):
    if not os.path.exists(input_path):
        raise Exception("Downloaded file missing before processing")
    output_name = str(uuid.uuid4())
    os.makedirs("outputs", exist_ok=True)

    if operation == "thumbnail":
        output_path = f"outputs/{output_name}.jpg"

        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-ss",
            "00:00:02",
            "-vframes",
            "1",
            output_path,
        ]

    elif operation == "compress":
        output_path = f"outputs/{output_name}.mp4"

        crf_map = {"low": "32", "medium": "28", "high": "23"}

        crf = crf_map.get(quality, "28")

        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            "scale=1280:-2",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-crf",
            crf,
            "-c:a",
            "copy",
            "-threads",
            "1",
            "-movflags",
            "+faststart",
            output_path,
        ]

    elif operation == "extract_audio":
        output_path = f"outputs/{output_name}.mp3"

        audio_bitrate = bitrate if bitrate else "128"

        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vn",
            "-acodec",
            "libmp3lame",
            "-b:a",
            f"{audio_bitrate}k",
            output_path,
        ]

    else:
        raise Exception("Invalid Operation")

    print("Running command:", command)

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=160
        )

        if result.returncode != 0:
            raise Exception(result.stderr.decode())

    except subprocess.TimeoutExpired:
        raise Exception("Processing timed out (file too large or slow)")

    return output_path
