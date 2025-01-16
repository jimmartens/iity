from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import firestore
import os
import random
import string

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    # allow_origins=["http://frontend-403359582991.us-central1.run.app:3000"],  # Production frontend URL
    # allow_origins=["*"],  # allow all
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Firestore emulator settings
project_id = "your-project-id"
firestore_host = os.getenv("FIRESTORE_EMULATOR_HOST", "localhost:8080")

# Initialize Firestore client
if os.getenv("USE_FIRESTORE_EMULATOR", "false").lower() == "true":
    db = firestore.Client(project=project_id)
else:
    # For production, use the default credentials
    db = firestore.Client.from_service_account_json('firestore-key.json')

class Guess(BaseModel):
    name: str
    content: str
    created_at: str = firestore.SERVER_TIMESTAMP

@app.post("/guesses")
async def create_guess(guess: Guess):
    try:
        doc_ref = db.collection("guesses").document()
        doc_ref.set(guess.model_dump())
        return {"message": "Guess added successfully", "id": doc_ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/guesses")
async def get_guesses():
    try:
        guesses = []
        for doc in db.collection("guesses").stream():
            guess_data = doc.to_dict()
            guess_data['id'] = doc.id
            guesses.append(guess_data)
        return guesses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
async def root():
    return {"message": "Welcome to the Guessing Game API"}

@app.post("/testguess")
async def test_guess():
    try:
        doc_ref = db.collection("guesses").document()
        test_guess_content = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        test_guess = Guess(name="Test User", content=test_guess_content)
        db.collection("guesses").document().set(test_guess.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)