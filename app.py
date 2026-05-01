import streamlit as st
from rag_engine import get_answer 

# 1. Page Configuration
st.set_page_config(page_title="Cyber Threat Intel", page_icon="🛡️", layout="wide")

# 2. Inject Custom CSS for Animations and Styling
st.markdown("""
<style>
    /* Glowing Animated Title */
    .cyber-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
        animation: subtle-glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes subtle-glow {
        from { filter: drop-shadow(0 0 2px rgba(0, 210, 255, 0.2)); }
        to { filter: drop-shadow(0 0 8px rgba(0, 210, 255, 0.6)); }
    }

    /* Pulsing Status Dot */
    .status-dot {
        height: 12px;
        width: 12px;
        background-color: #00d2ff;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 210, 255, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 210, 255, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 210, 255, 0); }
    }

    /* Chat Message Slide-in Animation */
    div[data-testid="stChatMessage"] {
        animation: slideUp 0.5s ease-out forwards;
        opacity: 0;
        transform: translateY(15px);
        border-radius: 10px;
        padding: 10px;
    }
    
    @keyframes slideUp {
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Customizing the Expander */
    div[data-testid="stExpander"] {
        border-left: 4px solid #3a7bd5;
        border-radius: 8px;
    }
            /* Floating Watermark */
    .watermark {
        position: fixed;
        bottom: 15px;
        right: 20px;
        opacity: 0.4;
        font-size: 0.85rem;
        color: #a0aec0;
        z-index: 9999;
        font-family: monospace;
        pointer-events: none; /* Ensures you can still click things behind it */
        user-select: none;
    }
</style>
""", unsafe_allow_html=True)

# 3. Custom Header Layout
st.markdown('<h1 class="cyber-title">🛡️ Cyber Intel Bot</h1>', unsafe_allow_html=True)
st.markdown('<p><span class="status-dot"></span><b>Systems Online:</b> Secure localized environment.</p>', unsafe_allow_html=True)
st.write("---")

# 4. Split screen layout
col1, col2 = st.columns([1, 2.5]) # Adjusted ratio to give chat more room

with col1:
    st.subheader("🚀 Mission Control")
    st.info("📚 **Knowledge Base Active**\n\nConnected to local NIST & CVE databases. Ready for querying.")
    st.write("---")
    
    # A more encouraging toggle
    dev_mode = st.toggle("🔍 Enable Threat Analyst Mode", value=True)
    if dev_mode:
        st.caption("✨ *Analyst mode active: Raw vector chunks will be displayed for maximum transparency.*")
    else:
        st.caption("*Standard response mode active.*")

with col2:
    st.subheader("💬 Incident Response Channel")
    
    # Initialize chat history with an encouraging first message
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome back! I am synced with your security manuals. How can I assist you in securing our systems today?"}
        ]

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a security question (e.g., 'What are CSF Profiles?')..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("Decrypting and scanning localized data... 🔐"):
                try:
                    data = get_answer(prompt)
                    answer = data["answer"]
                    sources = data["sources"]

                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    # Stylish Dev Mode Output
                    if dev_mode and sources:
                        with st.expander("🔬 View Raw Database Chunks"):
                            st.write("Here is exactly where I pulled that information from:")
                            for i, source in enumerate(sources):
                                st.info(f"**Data Node {i+1}:**\n\n{source}")
                                
                except Exception as e:
                    st.error(f"System Error: {e}")
# 5. Personal Watermark
st.markdown('<div class="watermark">Built by Krishna Dubey</div>', unsafe_allow_html=True)