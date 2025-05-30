import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.post("/remove-background/")
async def remove_bg(file: UploadFile = File(...)):
    contents = await file.read()
    output = remove(contents)
    image = Image.open(BytesIO(output)).convert("RGBA")
    img_io = BytesIO()
    image.save(img_io, format="PNG")
    img_io.seek(0)
    return StreamingResponse(img_io, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Render sets this
    uvicorn.run("main:app", host="0.0.0.0", port=port)
