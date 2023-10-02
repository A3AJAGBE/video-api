from fastapi.middleware.cors import CORSMiddleware
from whisper_transcribe import Transcriber
from fastapi import FastAPI, File, UploadFile
import os
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi

load_dotenv()

app = FastAPI(openapi_url="/api/v1/openapi.json",
              docs_url="/api/livedoc", redoc_url=None)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recording_path = []


# Get the path to the user's desktop directory
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

# Create the new folder on the desktop
BLOB_FOLDER_NAME = "BlobRecords"
BLOB_FOLDER_PATH = os.path.join(DESKTOP_PATH, BLOB_FOLDER_NAME)


try:
    os.makedirs(BLOB_FOLDER_PATH)
except FileExistsError:
    pass


NO_CONTENT_RESPONSE = "No saved recording YET."


@app.post("/api/upload", tags=["Screen Recording"])
async def upload_recording(file: UploadFile = File(...)):
    blob_file_path = os.path.join(BLOB_FOLDER_PATH, file.filename)

    try:
        with open(blob_file_path, "wb") as f:
            f.write(await file.read())
    except Exception:
        return {"message": "There was an error uploading the screen recording."}

    recording_path.append(blob_file_path)
    return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/api/recordings", tags=["Screen Recording"])
async def get_recordings():
    if len(contents) == 0:
        return {"message": NO_CONTENT_RESPONSE}

    return {"recordings": recording_path}


@app.get("/api/recording/recent", tags=["Screen Recording"])
async def get_recent_recording():
    try:
        contents = os.listdir(BLOB_FOLDER_PATH)

        # Sort based on modification time
        contents_sorted = sorted(contents, key=lambda x: os.path.getmtime(
            os.path.join(BLOB_FOLDER_PATH, x)), reverse=True)

        record_path = os.path.join(BLOB_FOLDER_PATH, contents_sorted[0])

        with Transcriber(api_key=os.getenv("ScreenAPI")) as t:
            transcription = t.transcribe(record_path)
        return {"file_name": contents_sorted[0], "src": record_path, "transcription": transcription}

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
