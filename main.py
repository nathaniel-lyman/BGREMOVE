import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from io import BytesIO
from PIL import Image

app = FastAPI(title="Background Removal API", version="1.0.0")

@app.get("/")
def root():
    """Health check endpoint for Render"""
    return {"message": "Background Removal API is running", "status": "healthy"}

@app.get("/health")
def health():
    """Additional health check endpoint"""
    return {"status": "healthy"}

@app.post("/remove-background/")
async def remove_bg(file: UploadFile = File(...)):
    """Remove background from uploaded image"""
    try:
        contents = await file.read()
        output = remove(contents)
        image = Image.open(BytesIO(output)).convert("RGBA")
        img_io = BytesIO()
        image.save(img_io, format="PNG")
        img_io.seek(0)
        return StreamingResponse(img_io, media_type="image/png")
    except Exception as e:
        return {"error": f"Failed to process image: {str(e)}"}

def _get_port() -> int:
    """Return the port for the web server.

    Render provides the ``PORT`` environment variable when starting the
    service. If it is not set or is not a valid integer, fall back to 10000.
    """
    try:
        return int(os.environ.get("PORT", "10000"))
    except (TypeError, ValueError):
        return 10000


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=_get_port())