from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path
import os

app = FastAPI()

# Get the user's desktop directory
DESKTOP_PATH = Path.home() / "Desktop"

# The folder name
FOLDER_NAME = "apiVideos"

# Create the folder if it doesn't exist
FOLDER_PATH = DESKTOP_PATH / FOLDER_NAME
FOLDER_PATH.mkdir(parents=True, exist_ok=True)


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = FOLDER_PATH / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File saved successfully to apiVideos folder on your desktop"}


@app.get("/api/videos")
async def get_folder_contents():
    contents = os.listdir(FOLDER_PATH)
    return {"folder_contents": contents}


@app.get("/api/video/recent")
async def get_recent_content():
    contents = os.listdir(FOLDER_PATH)

    # Sort based on modification time
    contents_sorted = sorted(contents, key=lambda x: os.path.getmtime(
        os.path.join(FOLDER_PATH, x)), reverse=True)

    return {"recent_file": contents_sorted[0]}
