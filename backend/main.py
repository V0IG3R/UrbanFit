# backend/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from bicep_curls import process_landmarks as process_bicep_curls
from deadlifts import process_landmarks as process_deadlifts
from lunges import process_landmarks as process_lunges
from pushups import process_landmarks as process_pushups
from situps import process_landmarks as process_situps
from squats import process_landmarks as process_squats

app = FastAPI(title="UrbanFit: Innovative Exercise Analysis API")

# Enable CORS so that the frontend can make requests to the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to UrbanFit API"}

@app.post("/landmarks/{exercise_name}")
async def process_exercise_landmarks(exercise_name: str, request: Request, tolerance: int = 10):
    data = await request.json()
    landmarks = data.get("landmarks")
    if not landmarks:
        return JSONResponse({"error": "No landmarks provided"}, status_code=400)
    
    if exercise_name == "bicep_curls":
        result = process_bicep_curls(landmarks, tolerance)
    elif exercise_name == "deadlifts":
        result = process_deadlifts(landmarks, tolerance)
    elif exercise_name == "lunges":
        result = process_lunges(landmarks, tolerance)
    elif exercise_name == "pushups":
        result = process_pushups(landmarks, tolerance)
    elif exercise_name == "situps":
        result = process_situps(landmarks, tolerance)
    elif exercise_name == "squats":
        result = process_squats(landmarks, tolerance)
    else:
        return JSONResponse({"error": "Exercise not found"}, status_code=404)
    
    return JSONResponse(result)
