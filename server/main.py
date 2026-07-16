from fastapi import FastAPI

app = FastAPI(title="AI Career Mentor API")

@app.get("/")
def read_root():
    return {"message": "AI Career Mentor API is running"}