# chat_interface.py
"""Simple chat interface for RAG chatbot"""

import streamlit as st
from datetime import datetime
import re
from typing import List

class ChatInterface:
    def __init__(self):
        """Initialize chat interface"""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
    
    def render_chat_interface(self, qa_system, retrieval_k=5, similarity_threshold=1.0):
        """Render the main chat interface"""
        # Chat input
        user_query = st.chat_input("💬 Ask about the Constitution...")
        
        # Handle quick question selection
        if hasattr(st.session_state, 'current_question'):
            user_query = st.session_state.current_question
            del st.session_state.current_question
        
        if user_query:
            self.process_user_query(user_query, qa_system, retrieval_k, similarity_threshold)
        
        # Display chat history
        self.display_chat_history()
    
    def process_user_query(self, query: str, qa_system, retrieval_k: int, similarity_threshold: float):
        """Process user query with RAG workflow"""
        # Add user message
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        with st.chat_message("user"):
            st.markdown(f"**[{timestamp}]** {query}")
        
        # Generate response
        with st.chat_message("assistant"):
            st.markdown("🔍 **Searching Constitution...**")
            
            with st.spinner("Finding relevant sections..."):
                try:
                    # Get relevant chunks
                    relevant_chunks, scores = qa_system.embedding_manager.search(query, k=retrieval_k)
                    
                    if relevant_chunks:
                        # Filter by similarity threshold
                        filtered_chunks = []
                        filtered_scores = []
                        
                        for chunk, score in zip(relevant_chunks, scores):
                            if score <= similarity_threshold:
                                filtered_chunks.append(chunk)
                                filtered_scores.append(score)
                        
                        if filtered_chunks:
                            st.success(f"✅ Found {len(filtered_chunks)} relevant sections!")
                            
                            # Show sources
                            st.markdown("📚 **Sources:**")
                            for i, (chunk, score) in enumerate(zip(filtered_chunks, filtered_scores)):
                                title = self.extract_title(chunk)
                                with st.expander(f"📖 {title} (Score: {score:.3f})"):
                                    st.markdown(chunk[:500] + "..." if len(chunk) > 500 else chunk)
                            
                            # Generate AI response
                            st.markdown("---")
                            st.markdown("🤖 **AI Response:**")
                            
                            with st.spinner("Generating answer..."):
                                answer = qa_system.ollama_client.generate_rag_response(query, filtered_chunks)
                                
                                if answer:
                                    st.markdown(f"**{answer}**")
                                    
                                    # Save to chat history
                                    st.session_state.chat_history.append({
                                        "timestamp": timestamp,
                                        "query": query,
                                        "answer": answer,
                                        "sources": filtered_chunks,
                                        "scores": filtered_scores
                                    })
                                else:
                                    st.error("❌ Failed to generate response")
                        else:
                            st.warning(f"⚠️ No sections met the similarity threshold ({similarity_threshold})")
                    else:
                        st.warning("⚠️ No relevant sections found")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    def extract_title(self, chunk: str) -> str:
        """Extract title from chunk"""
        title_match = re.search(r'(Article\s+\d+[A-Z]?|PART\s+[IVXLCDM]+)', chunk)
        return title_match.group(1) if title_match else "Section"
    
    def display_chat_history(self):
        """Display chat history"""
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 💬 Chat History")
            
            for chat in st.session_state.chat_history:
                with st.expander(f"**{chat['timestamp']}** - {chat['query'][:50]}..."):
                    st.markdown(f"**Question:** {chat['query']}")
                    st.markdown(f"**Answer:** {chat['answer']}")
                    
                    if chat['sources']:
                        st.markdown("**Sources:**")
                        for i, source in enumerate(chat['sources'][:3]):  # Show first 3 sources
                            st.markdown(f"{i+1}. {source[:100]}...")