import os
import requests 
import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Network Kill-Switches (Keep these!)
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

CHROMA_PATH = "./chroma_db"

@st.cache_resource
def load_database():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return db.as_retriever(search_kwargs={"k": 3})

def get_answer(query: str):
    # --- 1. SMART ROUTING: Intercept Greetings Instantly ---
    clean_query = query.strip().lower()
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "greetings", "hi there"]
    
    if clean_query in greetings:
        return {
            "answer": "Hello! I am your Context-Aware Cyber Intel Bot. How can I assist you with your security posture or NIST protocols today?",
            "sources": []
        }

    # --- 2. Load DB ---
    try:
        retriever = load_database()
    except Exception as e:
        return {"answer": f"🚨 CRASH AT DATABASE: {str(e)}", "sources": []}
    
    # --- 3. Retrieve Context ---
    try:
        docs = retriever.invoke(query)
        context_text = "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        return {"answer": f"🚨 CRASH AT RETRIEVAL: {str(e)}", "sources": []}

    # --- 4. Simplified Fallback Prompt for 3B Models ---
    system_instructions = """You are an elite Cybersecurity Incident Response AI. 
    First, try to answer the user's question using ONLY the provided Context.
    If the answer is NOT in the Context, use your general cybersecurity knowledge to answer, but you MUST start your response with this exact phrase: "⚠️ [Not found in local manuals] - "
    """

    user_message = f"Context:\n{context_text}\n\nQuestion:\n{query}"

    # --- 5. Network Call ---
    url = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "messages": [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3, 
        "max_tokens": 800
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
        else:
            answer = f"🚨 API ERROR: {response.status_code} - {response.text}"
    except Exception as e:
        answer = f"🚨 CRASH AT LM STUDIO NETWORK: {str(e)}"

    sources = [doc.page_content for doc in docs]
    return {"answer": answer, "sources": sources}