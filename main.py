import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image

app = FastAPI(title="Background Removal API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Background Removal API is running", "status": "healthy"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/test-rembg")
def test_rembg():
    """Test if rembg can be imported"""
    try:
        from rembg import remove
        return {"status": "success", "message": "rembg imported successfully"}
    except Exception as e:
        return {"status": "error", "message": f"rembg import failed: {str(e)}"}

@app.post("/remove-background/")
async def remove_bg(file: UploadFile = File(...)):
    """Remove background from uploaded image"""
    try:
        # Import rembg only when needed to avoid startup delays
        from rembg import remove
        
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
    """Return the port for the web server."""
    try:
        return int(os.environ.get("PORT", "10000"))
    except (TypeError, ValueError):
        return 10000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=_get_port())