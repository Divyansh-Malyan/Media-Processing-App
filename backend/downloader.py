import requests
import os
import uuid
MAX_FILE_SIZE = 30 * 1024 * 1024

def download_media(url):

    os.makedirs("downloads", exist_ok=True)
    filename = f"downloads/{uuid.uuid4()}.mp4"

    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if "video" not in content_type and "octet-stream" not in content_type:
        raise Exception("Invalid media URL (not a video)")

    total_size = 0

    with open(filename, 'wb') as file:
        for chunk in response.iter_content(1024 * 1024):
            if not chunk:
              continue

            total_size += len(chunk)

            if total_size > MAX_FILE_SIZE:
                file.close()
                os.remove(filename)
                raise Exception("File too large (max 30MB allowed)")

            file.write(chunk)
        
    return filename