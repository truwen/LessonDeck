from fastapi import FastAPI

app = FastAPI(title="LessonDeck")


@app.get("/")
def root():
    return {"message": "LessonDeck backend is running"}