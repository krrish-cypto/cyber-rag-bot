import os
import requests  # <-- The standard Python network library (Indestructible)
import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "./chroma_db"

def get_answer(query: str):
    # 1. Load Local Database securely
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    # 2. Retrieve Context from your PDFs
    docs = retriever.invoke(query)
    context_text = "\n\n".join(doc.page_content for doc in docs)

    # 3. Format the Prompt Manually
    prompt_text = f"""You are an elite Cybersecurity Incident Response AI. 
    Use the following pieces of retrieved context to answer the question. 
    If the answer is not in the context, say 'WARNING: Protocol not found in current manuals.'

    Context: {context_text}

    Question: {query}
    """

    # 4. NAKED PYTHON API CALL (Bypassing LangChain's buggy wrapper entirely)
    url = "http://127.0.0.1:1234/v1/chat/completions"
    payload = {
        "messages": [{"role": "user", "content": prompt_text}],
        "temperature": 0.2,
        "max_tokens": 800
    }
    headers = {"Content-Type": "application/json"}

    # This is a synchronous, brute-force request. It will not close until it gets an answer.
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
        else:
            answer = f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        answer = f"Critical Network Failure: Make sure LM Studio is running. Detail: {str(e)}"

    # 5. Return Data
    sources = [doc.page_content for doc in docs]
    return {"answer": answer, "sources": sources}