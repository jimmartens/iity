from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import firestore
import os
import random
import string
from typing import List, Optional

app = FastAPI()

origins = []
if os.getenv("ENVIRONMENT") == "prod":
    origins.append("https://frontend-403359582991.us-central1.run.app")
    #origins.append("*") # Allow all
else:
    origins.append("http://localhost:3000")

print(f"Environment: {os.getenv('ENVIRONMENT')}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Firestore emulator settings
project_id = "your-project-id"
firestore_host = os.getenv("FIRESTORE_EMULATOR_HOST", "localhost:8080")

# Initialize Firestore client
if os.getenv("USE_FIRESTORE_EMULATOR", "false").lower() == "true":
    print(f"Using Firestore emulator at {firestore_host}")
    db = firestore.Client(project=project_id)
else:
    # For production, use the default credentials
    print("Using production Firestore credentials")
    db = firestore.Client.from_service_account_json('firestore-key.json')

class Guess(BaseModel):
    name: str
    acronym: str
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
async def get_guesses(
    page: int = 1,
    pageSize: int = 10,
    acronym: Optional[str] = None
):
    try:
        guesses = []
        query = db.collection("guesses")

        if acronym:
            query = query.where("acronym", "==", acronym)
        
        # Pagination implementation
        start_at = (page -1) * pageSize
        query_stream = query.order_by('created_at', direction=firestore.Query.DESCENDING).offset(start_at).limit(pageSize).stream()
        
        for doc in query_stream:
            guess_data = doc.to_dict()
            guess_data['id'] = doc.id
            guesses.append(guess_data)
            
        # Calculate total for use in pagination
        total_query = db.collection("guesses")
        if acronym:
            total_query = total_query.where("acronym", "==", acronym)
        total = len([item for item in total_query.stream()])
                
        return {"guesses": guesses, "total": total, "page": page, "pageSize": pageSize}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/guesses/{guess_id}")
async def get_guess(guess_id: str):
    try:
        doc_ref = db.collection("guesses").document(guess_id)
        doc = doc_ref.get()
        if doc.exists:
            guess_data = doc.to_dict()
            guess_data['id'] = doc.id
            return guess_data
        else:
            raise HTTPException(status_code=404, detail="Guess not found")
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
        test_guess = Guess(name="Test User", content=test_guess_content, acronym="YCHJCT_TEST")
        db.collection("guesses").document().set(test_guess.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)