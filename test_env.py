import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API keys
pinecone_key = os.getenv("PINECONE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

# Print the first few characters of each key (for security)
print("Pinecone API Key loaded:", "Yes" if pinecone_key else "No")
if pinecone_key:
    print("Pinecone Key starts with:", pinecone_key[:4] + "..." if len(pinecone_key) > 4 else "Invalid length")

print("\nOpenAI API Key loaded:", "Yes" if openai_key else "No")
if openai_key:
    print("OpenAI Key starts with:", openai_key[:4] + "..." if len(openai_key) > 4 else "Invalid length") 