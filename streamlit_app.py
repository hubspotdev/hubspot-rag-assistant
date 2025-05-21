import streamlit as st
import requests
import json

st.set_page_config(
    page_title="HubSpot RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 HubSpot RAG Assistant")
st.markdown("Ask questions about HubSpot development and get answers based on the official documentation.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about HubSpot development..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    try:
        response = requests.post(
            "http://localhost:8000/ask",
            json={"question": prompt}
        )
        response.raise_for_status()
        result = response.json()

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(result["answer"])
            
            # Display sources in an expander
            with st.expander("View Sources"):
                for i, source in enumerate(result["sources"], 1):
                    st.markdown(f"**Source {i}:**")
                    st.markdown(source)
                    st.markdown("---")

        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"]
        })

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Make sure the FastAPI server is running at http://localhost:8000")
