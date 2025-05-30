from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is working", "status": "healthy"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/test")
def test():
    return {"test": "endpoint working"}