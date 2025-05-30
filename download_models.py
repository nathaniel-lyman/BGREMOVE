#!/usr/bin/env python3
"""Pre-download rembg models during build phase"""

import sys
from rembg import remove
from io import BytesIO
from PIL import Image

def download_models():
    """Download default rembg model by running a dummy operation"""
    print("Downloading rembg models...")
    
    # Create a small dummy image
    dummy_img = Image.new('RGB', (10, 10), color='red')
    img_bytes = BytesIO()
    dummy_img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # This will trigger model download
    try:
        remove(img_bytes.getvalue())
        print("✅ Models downloaded successfully!")
    except Exception as e:
        print(f"⚠️  Model download failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_models()
