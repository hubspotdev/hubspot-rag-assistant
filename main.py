from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="HubSpot RAG Assistant")

# Initialize OpenAI and Pinecone
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("hubspot-llms")

# Define request and response models
class Question(BaseModel):
    question: str

class Answer(BaseModel):
    question: str
    answer: str
    sources: List[str]

def get_embedding(text: str) -> list:
    """Generate OpenAI embedding for a given text."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def search_pinecone(vector: list, top_k: int = 5) -> list:
    """Query Pinecone with the embedding vector."""
    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )
    return results.get("matches", [])

def generate_answer(context: str, question: str) -> str:
    """Generate GPT-4 answer based on the context and question."""
    prompt = f"Use the following HubSpot documentation to answer the question.\n\n{context}\n\nQ: {question}\nA:"
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that only answers based on the HubSpot's Developer documentation."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    try:
        # Step 1: Get embedding for the question
        embedding = get_embedding(question.question)

        # Step 2: Search in Pinecone
        matches = search_pinecone(embedding)
        if not matches:
            raise HTTPException(status_code=404, detail="No relevant documentation found.")

        # Step 3: Generate answer using GPT-4
        context = "\n\n".join([m["metadata"]["text"] for m in matches])
        answer = generate_answer(context, question.question)

        # Step 4: Return response
        return Answer(
            question=question.question,
            answer=answer,
            sources=[m["metadata"]["text"] for m in matches]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the HubSpot RAG Assistant API"}
