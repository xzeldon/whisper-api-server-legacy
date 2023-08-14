import os
import shutil
import torch
import uvicorn

from threading import Lock
from typing import Union, Optional

from fastapi import FastAPI, Form, HTTPException, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel

SERVER_PORT = 8000
UPLOAD_DIR = "tmp"
MODEL_NAME = "medium"

WHISPER_OPTIONS = {
    "task": "translate",
    "language": "ru",
    "temperature": 0.0,
    "temperature_increment_on_fallback": 0.2,
    "no_speech_threshold": 0.6,
    "logprob_threshold": -1.0,
    "compression_ratio_threshold": 2.4,
    "condition_on_previous_text": True,
    "verbose": False,
}


if torch.cuda.is_available():
    model = WhisperModel(MODEL_NAME, device="cuda", compute_type="float32")
else:
    model = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8")

model_lock = Lock()

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    print(f"Upload dir created: {UPLOAD_DIR}")
else:
    print(f"Upload dir: {UPLOAD_DIR}")

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def transcribe(
    file,
    task: Union[str, None],
    language: Union[str, None],
    **whisper_options,
):
    whisper_options = {"task": task}

    if language:
        whisper_options["language"] = language

    with model_lock:
        segments = []
        text = ""
        segment_generator, info = model.transcribe(file, beam_size=5, **whisper_options)
        for segment in segment_generator:
            segments.append(segment)
            text = text + segment.text
        result = {
            "language": whisper_options.get("language", info.language),
            "segments": segments,
            "text": text,
        }

        return result


@app.post("/v1/audio/transcriptions")
async def transcriptions(
    file: UploadFile = File(...),
    model: str = Form(...),
    language: Optional[str] = Form(None),
):
    assert model == "whisper-1"

    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad file")

    filename = file.filename
    fileobj = file.file
    upload_name = os.path.join(UPLOAD_DIR, filename)
    upload_file = open(upload_name, "wb+")
    shutil.copyfileobj(fileobj, upload_file)
    upload_file.close()

    transcript = transcribe(file=upload_name, **WHISPER_OPTIONS)
    return {"text": transcript["text"].replace(" ", "", 1)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
