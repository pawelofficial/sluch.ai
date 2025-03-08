from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime 
import time 
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


class TranscribeRequest(BaseModel):
    text: str

@app.post("/transcribe")
async def transcribe(req: TranscribeRequest):
    ts_now = datetime.datetime.now().isoformat()
    response_text = f'received {req.text} {ts_now}'
    print(response_text)
    return JSONResponse(content={"text": response_text})

class User(BaseModel):
    username: str
    password : str 


@app.post("/login")
async def transcribe(req: User):
    if req.username.lower()=='admin' and req.password.lower()=='admin':
        return JSONResponse(content={"text": f"Welcom {req.username} !","success":True })
    else:
        return JSONResponse(content={"text": "invalid username/password","success":False })

@app.post("/register")
async def transcribe(req: User):
    if req.username.lower()=='admin' and req.password.lower()=='admin':
        return JSONResponse(content={"text": f"{req.username} ","success":True })
    else:
        return JSONResponse(content={"text": "invalid username/password","success":False })




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
