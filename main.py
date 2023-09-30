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

NO_CONTENT_RESPONSE = "No saved record YET."


@app.post("/api/upload")
async def upload_screen_record(file: UploadFile = File(...)):
    file_path = FOLDER_PATH / file.filename

    try:
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the screen recording."}

    return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/api/videos")
async def get_folder_contents():
    contents = os.listdir(FOLDER_PATH)

    if len(contents) == 0:
        return {"message": NO_CONTENT_RESPONSE}
    else:
        return {"folder_contents": contents}


@app.get("/api/video/recent")
async def get_recent_content():
    try:
        contents = os.listdir(FOLDER_PATH)

        # Sort based on modification time
        contents_sorted = sorted(contents, key=lambda x: os.path.getmtime(
            os.path.join(FOLDER_PATH, x)), reverse=True)

        return {"recent_file": contents_sorted[0]}

    except IndexError:
        return {"message": NO_CONTENT_RESPONSE}
