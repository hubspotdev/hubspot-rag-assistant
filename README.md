# HubSpot RAG Assistant

This project is a Retrieval-Augmented Generation (RAG) assistant for HubSpot documentation. It uses OpenAI to generate embeddings, Pinecone to store and search relevant document chunks, and FastAPI to serve a query endpoint.

---

## 🧩  Features

* Embeds HubSpot documentation from [`llms-full.txt`](https://developers.hubspot.com/docs/llms-full.txt)
* Generates OpenAI embeddings and stores them in Pinecone
* Provides a FastAPI endpoint to query the documents using semantic search
* Optional: Streamlit interface for easy testing

---

## 🗂️ Project Structure

```
hubspot-rag-app/
├── llms-full.txt              # Raw documentation source
├── embed.py                   # Script to chunk and embed data into Pinecone
├── query.py                   # Command-line interface for querying the RAG system
├── main.py                    # FastAPI backend for querying and answering
├── streamlit_app.py           # Optional Streamlit UI for local testing
├── .env                       # API keys and config
├── requirements.txt           # Dependencies
```

---

## ⚙️ Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd hubspot-rag-assistant
```

2. Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENV=your-pinecone-environment
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🔧 Populate Pinecone

To generate and store embeddings from the HubSpot documentation:

```bash
python embed.py
```

This script:

* Loads `llms-full.txt`
* Splits it into chunks
* Generates OpenAI embeddings
* Stores them in Pinecone with IDs

---

## 🚀 Running the Application

### Start the FastAPI Backend

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Start the Streamlit Interface

In a new terminal:
```bash
streamlit run streamlit_app.py
```

The Streamlit interface will be available at `http://localhost:8501`

---

## 🧪 Test with [Postman](https://www.postman.com/hubspot/workspace/hubspot-developer-use-cases/collection/26126890-eac4b338-fd98-42b9-93f6-dd46a71d8f72?action=share&source=copy-link&creator=26126890)

### Endpoint

```
POST http://localhost:8000/ask
```

### Request Body

```json
{
  "question": "What are developer test accounts in HubSpot?"
}
```

### Response

```json
{
  "question": "What are developer test accounts in HubSpot?",
  "answer": "Developer test accounts are free HubSpot environments that allow you to test apps and integrations...",
  "sources": [
    "Developer test accounts will expire after 90 days if no API calls...",
    "You can create up to 10 test accounts per developer account..."
  ]
}
```

---

## 💡 Optional: Streamlit UI

To test locally with a simple web interface:

```bash
streamlit run streamlit_app.py
```

You'll get a local UI where you can enter questions and see answers and source snippets like in the example below:

![Streamlit UI Example](https://github.com/hubspotdev/hubspot-rag-assistant/blob/3e9166e5c163c1f422226a5054e5bc3f618fe0c8/HubSpotRAGAssistantUIDemo.gif)
---

## 🧐 Technologies Used

* [OpenAI](https://platform.openai.com/docs)
* [Pinecone](https://www.pinecone.io/)
* [LangChain](https://www.langchain.com/langchain)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Streamlit](https://streamlit.io/) *(optional)*

---

## 📌 Roadmap

* [ ] Add auth and usage limits
* [ ] Deploy to cloud (e.g., Render/Fly.io)
* [ ] Enable document updates/re-indexing

---

## 🙌 Credits

* HubSpot Developer Docs: [https://developers.hubspot.com/docs](https://developers.hubspot.com/docs)
* Built with OpenAI, Pinecone, FastAPI

## 💻 Command-Line Interface

For quick testing or integration with other tools, you can use the command-line interface:

```bash
python3 query.py
```

The CLI will:
1. Prompt you to enter a question
2. Show the most relevant documentation chunks
3. Optionally generate a GPT-4 answer based on the chunks

Example usage:
```bash
Ask a question about HubSpot development: What are developer test accounts?
🔍 Top Chunks:
[Shows relevant documentation chunks]

🧠 Use GPT-4 to generate answer from these chunks? (y/n): y
✅ Answer:
[Shows generated answer]
```

## 🐛 Troubleshooting

1. If you see "command not found" errors:
   - Verify all dependencies are installed (`pip install -r requirements.txt`)
