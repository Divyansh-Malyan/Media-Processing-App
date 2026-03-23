# Media Processing App

This is a full-stack media processing application that allows users to process videos directly from a URL. The app can generate thumbnails, compress videos, and extract audio using FFmpeg.

The goal of this project was to build a simple but robust system that handles real-world scenarios like large files, invalid inputs, and processing failures.

---

## What this app does

* Accepts a media (video) URL
* Lets the user choose an operation:

  * Generate thumbnail
  * Compress video
  * Extract audio
* Processes the media using FFmpeg (via Python subprocess)
* Displays the result directly in the UI

---

## Tech Stack

* **Frontend:** React (Vite)
* **Backend:** FastAPI (Python)
* **Media Processing:** FFmpeg (via subprocess)
* **HTTP:** Fetch API

---

## How it works

1. User enters a video URL and selects an operation
2. Frontend sends a request to the backend (`/process`)
3. Backend:

   * Downloads the media file temporarily
   * Runs an FFmpeg command based on the selected operation
   * Stores the output in the `outputs` folder
4. Backend returns a URL to the processed file
5. Frontend displays the result (image/video/audio player)

---

## API

### POST `/process`

**Request:**

```json
{
  "url": "https://example.com/video.mp4",
  "operation": "thumbnail"
}
```

**Optional fields:**

```json
{
  "quality": "low | medium | high",
  "bitrate": "64 | 128 | 320"
}
```

**Success Response:**

```json
{
  "status": "success",
  "output_url": "/outputs/file-name.mp4"
}
```

**Error Response:**

```json
{
  "status": "error",
  "message": "error details"
}
```

---

## Async Processing (Bonus)

There is also an additional endpoint:

### POST `/process-async`

* Starts processing in the background
* Returns immediately without waiting for FFmpeg

This was added to demonstrate non-blocking processing using FastAPI’s `BackgroundTasks`.

---

## Error Handling & Safety

The backend handles several real-world edge cases:

* Invalid or unreachable URLs
* Unsupported file formats
* FFmpeg processing errors
* Timeout handling (to avoid long-running processes)
* File size limit (30MB max)

---

## Performance Considerations

* Files are downloaded in chunks (memory efficient)
* Large files are rejected early
* Temporary files are cleaned up automatically
* Old output files are deleted periodically

---

## Project Structure

```
Media-Processing-App/
│
├── backend/
│   ├── main.py
│   ├── downloader.py
│   ├── processor.py
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│
└── README.md
```

---

## Setup Instructions

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Sample Test URL

You can test using a public video URL like:

```
https://filesamples.com/samples/video/mp4/sample_640x360.mp4
```

---

## Output

* Thumbnail → Image preview
* Compress → Video player
* Extract Audio → Audio player

---

## Assumptions

* Only video URLs are supported
* Files larger than 30MB are rejected
* Output files are stored temporarily (no persistent storage)

---
