import os
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import ServerlessSpec

# Load .env variables
load_dotenv()

# Set up API keys
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Connect to Pinecone index (create one if it doesn't exist)
index_name = "hubspot-llms"

# Delete existing index if it exists
if index_name in pc.list_indexes().names():
    print(f"Deleting existing index '{index_name}'...")
    pc.delete_index(index_name)

# Create new index
print(f"Creating new index '{index_name}'...")
pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
index = pc.Index(index_name)

# Step 1: Load text
with open("llms-full.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# Step 2: Split text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(full_text)

# Step 3: Generate embeddings and upsert to Pinecone
for i, chunk in enumerate(chunks):
    print(f"Embedding chunk {i+1}/{len(chunks)}")
    embedding = client.embeddings.create(
        input=chunk,
        model="text-embedding-3-small"
    ).data[0].embedding

    # Step 4: Upsert to Pinecone
    index.upsert([
        (f"chunk-{i}", embedding, {"text": chunk})
    ])

print(f"✅ Finished embedding {len(chunks)} chunks into Pinecone.")
