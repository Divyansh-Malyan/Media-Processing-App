import requests
import os
import uuid

def download_media(url):

    os.makedirs("downloads", exist_ok=True)
    filename = f"downloads/{uuid.uuid4()}.mp4"

    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if "video" not in content_type:
        raise Exception("Invalid media URL (not a video)")

    with open(filename, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
        
    return filename