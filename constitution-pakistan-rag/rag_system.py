# rag_system.py
"""Simple RAG system for Constitution chatbot"""

import os
import fitz  # PyMuPDF
import streamlit as st
from document_processor import DocumentProcessor
from embedding_manager import EmbeddingManager
from ollama_client import OllamaClient
from config import EMBEDDINGS_DIR

class RAGSystem:
    def __init__(self):
        """Initialize RAG system"""
        self.doc_processor = DocumentProcessor()
        self.embedding_manager = EmbeddingManager()
        self.ollama_client = OllamaClient()
        self.initialized = False
    
    def initialize_system(self) -> bool:
        """Initialize the RAG system"""
        try:
            print("🔄 Initializing RAG system...")
            
            # Process document
            if not self._process_document():
                return False
            
            # Initialize embedding manager
            if not self._initialize_embedding_manager():
                return False
            
            # Test Ollama connection
            print("🔍 Testing Ollama connection...")
            if self.ollama_client.check_connection():
                print("✅ Ollama connected!")
                
                if self.ollama_client.check_model_availability():
                    print("✅ DeepSeek Coder model available!")
                else:
                    print("⚠️ DeepSeek Coder model not found")
            else:
                print("⚠️ Ollama not connected")
            
            print("✅ RAG system initialized!")
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            return False
    
    def _process_document(self) -> bool:
        """Process the document"""
        try:
            print("📄 Processing document...")
            text = self.doc_processor.load_document()
            chunks = self.doc_processor.chunk_document(text)
            
            stats = self.doc_processor.get_chunk_stats()
            print(f"✅ Document processed: {stats['total_chunks']} chunks created")
            
            return True
        except Exception as e:
            print(f"❌ Document processing failed: {e}")
            return False
    
    def _initialize_embedding_manager(self) -> bool:
        """Initialize embedding manager"""
        try:
            print("🔍 Loading embedding model...")
            self.embedding_manager.load_model()
            print("✅ Embedding model loaded!")
            
            # Try to load existing embeddings
            embeddings_file = os.path.join(EMBEDDINGS_DIR, "constitution_embeddings.pkl")
            
            if self.embedding_manager.load_embeddings(embeddings_file):
                print("✅ Embeddings loaded from cache")
            else:
                print("🔄 Creating new embeddings...")
                chunks = self.doc_processor.get_chunks()
                
                if chunks:
                    self.embedding_manager.create_embeddings(chunks)
                    self.embedding_manager.create_faiss_index()
                    print("✅ New embeddings created!")
                else:
                    print("❌ No chunks available")
                    return False
            
            return True
        except Exception as e:
            print(f"❌ Embedding manager initialization failed: {e}")
            return False
    
    def answer_question(self, query: str) -> tuple:
        """Answer a question using RAG"""
        try:
            if not self.initialized:
                return "System not initialized", [], []
            
            # Get relevant chunks
            relevant_chunks, scores = self.embedding_manager.search(query, k=5)
            
            if not relevant_chunks:
                return "No relevant information found", [], []
            
            # Generate response
            answer = self.ollama_client.generate_rag_response(query, relevant_chunks)
            
            if not answer:
                return "Failed to generate response", [], []
            
            return answer, relevant_chunks, scores
            
        except Exception as e:
            print(f"❌ Error answering question: {e}")
            return f"An error occurred: {str(e)}", [], []
    
    def display_system_status(self):
        """Display system status"""
        if self.initialized:
            st.success("✅ RAG System Ready")
            
            # Show basic stats
            col1, col2 = st.columns(2)
            with col1:
                doc_stats = self.doc_processor.get_chunk_stats()
                st.metric("Document Chunks", doc_stats.get('total_chunks', 0))
            
            with col2:
                emb_stats = self.embedding_manager.get_embedding_stats()
                st.metric("Embeddings", emb_stats.get('faiss_index_size', 0))
        else:
            st.warning("⚠️ System not initialized")