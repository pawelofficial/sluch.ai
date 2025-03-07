from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/audio")
async def receive_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    print(f"Received audio length: {len(audio_bytes)} bytes")
    return {"length_bytes": len(audio_bytes)}

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)