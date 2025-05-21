import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Initialize OpenAI and Pinecone clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("hubspot-llms")

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

def main():
    # Get user question
    question = input("Ask a question about HubSpot development: ").strip()

    # Step 1: Get embedding
    embedding = get_embedding(question)

    # Step 2: Search in Pinecone
    matches = search_pinecone(embedding)
    if not matches:
        print("⚠️ No relevant chunks found.")
        return

    # Step 3: Show top matches
    print("\n🔍 Top Chunks:")
    for i, match in enumerate(matches, start=1):
        print(f"\nChunk {i}:\n{match['metadata']['text']}")

    # Step 4: Optionally use GPT to summarize
    use_gpt = input("\n🧠 Use GPT-4 to generate answer from these chunks? (y/n): ").lower()
    if use_gpt == "y":
        context = "\n\n".join([m["metadata"]["text"] for m in matches])
        answer = generate_answer(context, question)
        print(f"\n✅ Answer:\n{answer}")

if __name__ == "__main__":
    main()
