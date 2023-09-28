from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

app = FastAPI()

# Get the user's desktop directory
DESKTOP_PATH = Path.home() / "Desktop"

# The folder name
FOLDER_NAME = "apiVideos"

# Create the folder if it doesn't exist
PATH_TO_FOLDER = DESKTOP_PATH / FOLDER_NAME
PATH_TO_FOLDER.mkdir(parents=True, exist_ok=True)


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = PATH_TO_FOLDER / file.filename

    # Open the file in binary write mode and copy the contents of the uploaded file to it
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File saved successfully to apiVideos folder on your desktop"}

# @app.get("/")
# def root():
#     return {"message": "Welcome A3!!"}


# @app.post("/api/upload/")
# async def upload_file(file: UploadFile):
#     return {"filename": file.filename}
