from fastapi import FastAPI
from pydantic import BaseModel
from downloader import download_media
from processor import process_media
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

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


@app.post("/process")
def process(request: MediaRequest):
    try:
        input_path = download_media(request.url)
        output_path = process_media(
            input_path, request.operation, request.quality, request.bitrate
        )

       

        return {
            "status": "success",
            "output_url": f"/outputs/{output_path.split('/')[-1]}",
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
         if os.path.exists(input_path):
            os.remove(input_path)