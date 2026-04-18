import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()

CHROMA_PATH = "./chroma_db"

def get_answer(query: str):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = ChatGroq(
        temperature=0.2, 
        model_name="llama3-8b-8192", 
        api_key=os.getenv("GROQ_API_KEY")
    )

    system_prompt = (
        "You are an elite Cybersecurity Incident Response AI. "
        "Use the following pieces of retrieved context to answer the question. "
        "If the answer is not in the context, say 'WARNING: Protocol not found in current manuals.'\n\n"
        "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    response = rag_chain.invoke({"input": query})
    
    # Extract the answer and the sources used
    answer = response["answer"]
    sources = [doc.page_content for doc in response["context"]]
    
    return {"answer": answer, "sources": sources}