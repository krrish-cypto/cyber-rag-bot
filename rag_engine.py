import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

CHROMA_PATH = "./chroma_db"

def get_answer(query: str):
    # 1. Setup DB
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # 2. Setup LLM
    llm = ChatGroq(
        temperature=0.2, 
        model_name="llama-3.1-8b-instant",  # <-- Update this line
        api_key=os.getenv("GROQ_API_KEY")
    )

    # 3. Setup Prompt
    template = """You are an elite Cybersecurity Incident Response AI. 
    Use the following pieces of retrieved context to answer the question. 
    If the answer is not in the context, say 'WARNING: Protocol not found in current manuals.'

    Context: {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 4. Retrieve documents directly
    docs = retriever.invoke(query)
    context_text = "\n\n".join(doc.page_content for doc in docs)

    # 5. Generate Answer (Using bulletproof LCEL syntax)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context_text, "question": query})
    
    # 6. Return Data
    sources = [doc.page_content for doc in docs]
    return {"answer": answer, "sources": sources}