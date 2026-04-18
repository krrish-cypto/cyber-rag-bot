import streamlit as st
import requests

st.set_page_config(page_title="Cyber Threat Intel", layout="wide")

st.title("🛡️ Context-Aware Cyber Intel Bot")

# Split screen layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("System Controls")
    st.info("Knowledge Base: Active (NIST Framework & CVE Docs)")
    st.write("---")
    # The evaluation panel "wow" factor
    dev_mode = st.toggle("Enable Developer Context Mode", value=True)
    st.caption("Shows exact vector chunks retrieved from ChromaDB.")

with col2:
    st.subheader("Incident Response Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Query security protocols..."):
        # Add user message to UI
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call FastAPI backend
        with st.chat_message("assistant"):
            with st.spinner("Scanning security playbooks..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/chat", 
                        json={"query": prompt}
                    )
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]

                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    # Show sources if dev mode is on
                    if dev_mode and sources:
                        with st.expander("🔍 View Retrieved Vector Chunks"):
                            for i, source in enumerate(sources):
                                st.markdown(f"**Chunk {i+1}:**\n{source}")
                                st.write("---")
                                
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")