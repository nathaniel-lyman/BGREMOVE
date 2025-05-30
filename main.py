from fastapi import FastAPI, UploadFile, File
from gradio_client import Client
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI()
client = Client("tehnateh/background-remover")

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = client.predict(image_bytes, api_name="/predict")
    return StreamingResponse(BytesIO(result.read()), media_type="image/png")
