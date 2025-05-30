import os
import asyncio
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO

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
        from rembg import remove  # noqa: F401
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
        output = await asyncio.to_thread(remove, contents)
        return StreamingResponse(BytesIO(output), media_type="image/png")
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