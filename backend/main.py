from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from downloader import download_media
from processor import process_media
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import time

app = FastAPI()

os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MediaRequest(BaseModel):
    url: str
    operation: str
    quality: str | None = None
    bitrate: str | None = None


def clean_old_outputs():
    folder = "outputs"

    if not os.path.exists(folder):
        return

    now = time.time()

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path):
            if now - os.path.getmtime(path) > 600:
                os.remove(path)


def clean_downloads():
    folder = "downloads"

    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path):
            os.remove(path)


def process_in_background(request: MediaRequest, input_path: str):
    try:
        process_media(
            input_path,
            request.operation,
            request.quality,
            request.bitrate
        )
    finally:
        if input_path and os.path.exists(input_path):
            os.remove(input_path)


@app.post("/process")
def process(request: MediaRequest):
    input_path = None

    try:
        clean_old_outputs()
        clean_downloads()

        input_path = download_media(request.url)

        output_path = process_media(
            input_path,
            request.operation,
            request.quality,
            request.bitrate
        )

        return {
            "status": "success",
            "output_url": f"/outputs/{output_path.split('/')[-1]}",
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        if input_path and os.path.exists(input_path):
            os.remove(input_path)


@app.post("/process-async")
def process_async(request: MediaRequest, background_tasks: BackgroundTasks):
    input_path = None

    try:
        clean_old_outputs()
        clean_downloads()

        input_path = download_media(request.url)

        background_tasks.add_task(process_in_background, request, input_path)

        return {
            "status": "success",
            "message": "Processing started in background"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }