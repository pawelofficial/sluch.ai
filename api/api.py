from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import datetime 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (for testing only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/audio")
async def receive_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    ts_now=datetime.datetime.now().isoformat()
    text = f'Lorem ipsum dolor sit amet, consectetur adipiscing elit {ts_now} '
    print(text)
    return JSONResponse(content={"text": text})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
