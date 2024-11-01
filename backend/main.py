from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import firestore
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
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
        doc_ref.set(guess.dict())
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)