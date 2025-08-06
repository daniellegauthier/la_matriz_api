from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.models import PhraseRequest, PhraseResponse
from app.pipeline import initialize_pipeline, process_phrase
from app.utils import generate_visualization
import uuid
import os

app = FastAPI()

# Allow CORS (if you build a frontend or want API access from browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for serving images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize pipeline
pipeline = initialize_pipeline()

@app.get("/")
def read_root():
    return {"message": "Semantic Color Phrase API is running!"}

@app.post("/analyze", response_model=PhraseResponse)
def analyze_phrase(request: PhraseRequest):
    try:
        result = process_phrase(
            pipeline=pipeline,
            phrase=request.phrase,
            length=request.length,
            momentum=request.momentum
        )

        # Save visualization
        image_id = str(uuid.uuid4())
        image_path = f"app/static/images/{image_id}.png"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        generate_visualization(
            rgb_sequence=result['rgb_sequence'],
            momentum=result['momentum'],
            pipeline=pipeline,
            input_phrase=request.phrase,
            filepath=image_path
        )

        return PhraseResponse(
            seed_words=result['seed_words'],
            rgb_sequence=result['rgb_sequence'],
            image_url=f"/static/images/{image_id}.png"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
