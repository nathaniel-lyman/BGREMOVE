from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.post("/remove-background/")
async def remove_bg(file: UploadFile = File(...)):
    # Read the uploaded file
    contents = await file.read()
    
    # Remove background
    output = remove(contents)

    # Convert output to a streamable format
    image = Image.open(BytesIO(output)).convert("RGBA")
    img_io = BytesIO()
    image.save(img_io, format="PNG")
    img_io.seek(0)

    return StreamingResponse(img_io, media_type="image/png")
