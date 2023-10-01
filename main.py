from whisper_transcribe import Transcriber
from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path
import os
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi

load_dotenv()

app = FastAPI(openapi_url="/api/v1/openapi.json",
              docs_url="/api/livedoc", redoc_url=None)

# Get the user's desktop directory
DESKTOP_PATH = Path.home() / "Desktop"

# The folder name
FOLDER_NAME = "Records"

# Create the folder if it doesn't exist
FOLDER_PATH = DESKTOP_PATH / FOLDER_NAME
FOLDER_PATH.mkdir(parents=True, exist_ok=True)

NO_CONTENT_RESPONSE = "No saved record YET."


@app.post("/api/upload", tags=["Screen Recording"])
async def upload_screen_record(file: UploadFile = File(...)):
    file_path = FOLDER_PATH / file.filename

    try:
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the screen recording."}

    return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/api/videos", tags=["Screen Recording"])
async def get_folder_contents():
    contents = os.listdir(FOLDER_PATH)

    if len(contents) == 0:
        return {"message": NO_CONTENT_RESPONSE}
    else:
        return {"folder_contents": contents}


@app.get("/api/video/recent", tags=["Screen Recording"])
async def get_recent_content():
    try:
        contents = os.listdir(FOLDER_PATH)

        # Sort based on modification time
        contents_sorted = sorted(contents, key=lambda x: os.path.getmtime(
            os.path.join(FOLDER_PATH, x)), reverse=True)

        record_path = str(FOLDER_PATH/contents_sorted[0])

        with Transcriber(api_key=os.getenv("ScreenAPI")) as t:
            transcription = t.transcribe(record_path)
        return {"recent_file": contents_sorted[0], "transcription": transcription}

    except IndexError:
        return {"message": NO_CONTENT_RESPONSE}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Screen Record API",
        version="1.0.0",
        summary="This is a RESTful API with partial CRUD functionality",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
