# main.py
"""Simple RAG Chatbot for Constitution of Pakistan"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chat_interface import ChatInterface
from rag_system import RAGSystem

def main():
    """Main application"""
    
    # Page config
    st.set_page_config(
        page_title="Constitution Assistant",
        page_icon="🇵🇰",
        layout="wide"
    )
    
    # Header
    st.title("🇵🇰 Constitution of Pakistan Assistant")
    st.markdown("Ask questions about the Constitution and get AI-powered answers with sources.")
    
    # Initialize RAG system
    if "rag_system" not in st.session_state:
        st.session_state.rag_system = RAGSystem()
        st.session_state.system_initialized = False
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Initialize button
        if not st.session_state.system_initialized:
            if st.button("🚀 Initialize System", type="primary", use_container_width=True):
                with st.spinner("Setting up system..."):
                    success = st.session_state.rag_system.initialize_system()
                    st.session_state.system_initialized = success
                    if success:
                        st.rerun()
        else:
            st.success("✅ System Ready!")
            if st.button("🔄 Reload", use_container_width=True):
                st.session_state.system_initialized = False
                st.rerun()
        
        # Settings
        st.subheader("🔧 Settings")
        retrieval_k = st.slider("Number of sources", 3, 10, 5)
        similarity_threshold = st.slider("Similarity threshold", 0.5, 2.0, 1.0, 0.1)
        
        # Quick questions
        st.subheader("❓ Quick Questions")
        questions = [
            "What is the state religion?",
            "What are fundamental rights?",
            "How is the Prime Minister appointed?",
            "What are the powers of the Supreme Court?"
        ]
        
        for q in questions:
            if st.button(q, use_container_width=True):
                st.session_state.current_question = q
    
    # Main content
    if st.session_state.system_initialized:
        # Chat interface
        chat_interface = ChatInterface()
        chat_interface.render_chat_interface(st.session_state.rag_system, retrieval_k, similarity_threshold)
    else:
        # Welcome message
        st.info("👋 Welcome! Click 'Initialize System' to get started.")
        
        # Simple setup guide
        with st.expander("📋 Quick Setup"):
            st.markdown("""
            1. **Install Ollama** from [ollama.ai](https://ollama.ai)
            2. **Pull the model**: `ollama pull deepseek-r1:latest`
            3. **Start Ollama**: `ollama serve`
            4. **Click Initialize System** above
            """)

if __name__ == "__main__":
    main()