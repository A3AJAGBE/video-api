from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome A3!!"}


@app.post("/api/upload/")
async def upload_file(file: UploadFile):
    return {"filename": file.filename}
