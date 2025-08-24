# embedding_manager.py
"""Simple embedding manager for RAG chatbot"""

import pickle
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDINGS_DIR, EMBEDDING_MODEL

class EmbeddingManager:
    def __init__(self):
        """Initialize embedding manager"""
        self.model = None
        self.embeddings = None
        self.chunks = []
        self.index = None
        self.model_name = EMBEDDING_MODEL
    
    def load_model(self):
        """Load the embedding model"""
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
    
    def create_embeddings(self, chunks: list):
        """Create embeddings for chunks"""
        if not chunks:
            raise ValueError("No chunks provided")
        
        # Filter out empty chunks
        valid_chunks = [chunk for chunk in chunks if chunk.strip()]
        if not valid_chunks:
            raise ValueError("No valid chunks after filtering")
        
        self.chunks = valid_chunks
        
        # Create embeddings
        self.embeddings = self.model.encode(valid_chunks, show_progress_bar=True)
        print(f"✅ Created embeddings: {self.embeddings.shape}")
    
    def create_faiss_index(self, embeddings=None):
        """Create FAISS index"""
        if embeddings is None:
            embeddings = self.embeddings
        
        if embeddings is None or len(embeddings) == 0:
            raise ValueError("No embeddings available")
        
        try:
            import faiss
            
            # Ensure embeddings are float32
            embeddings = embeddings.astype(np.float32)
            
            # Create index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
            self.index.add(embeddings)
            
            print(f"✅ FAISS index created: {self.index.ntotal} vectors")
            return self.index
            
        except Exception as e:
            print(f"❌ Error creating FAISS index: {e}")
            raise
    
    def load_embeddings(self, filepath: str) -> bool:
        """Load embeddings from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    data = pickle.load(f)
                    self.embeddings = data['embeddings']
                    self.chunks = data['chunks']
                    
                    # Recreate FAISS index
                    if self.embeddings is not None:
                        self.create_faiss_index()
                    
                    return True
            return False
        except Exception as e:
            print(f"❌ Error loading embeddings: {e}")
            return False
    
    def save_embeddings(self, filepath: str):
        """Save embeddings to file"""
        try:
            if self.embeddings is not None:
                data = {
                    'embeddings': self.embeddings,
                    'chunks': self.chunks
                }
                
                with open(filepath, 'wb') as f:
                    pickle.dump(data, f)
                
                print(f"✅ Embeddings saved to {filepath}")
        except Exception as e:
            print(f"❌ Error saving embeddings: {e}")
    
    def search(self, query: str, k: int = 5):
        """Search for similar chunks"""
        if self.index is None or self.embeddings is None:
            return [], []
        
        try:
            # Encode query
            query_embedding = self.model.encode([query])
            
            # Search
            scores, indices = self.index.search(query_embedding, k)
            
            # Get results
            results = []
            result_scores = []
            
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.chunks):
                    results.append(self.chunks[idx])
                    result_scores.append(score)
            
            return results, result_scores
            
        except Exception as e:
            print(f"❌ Error in search: {e}")
            return [], []
    
    def get_embedding_stats(self) -> dict:
        """Get embedding statistics"""
        stats = {
            "total_chunks": len(self.chunks) if hasattr(self, 'chunks') else 0,
            "embedding_dimension": self.embeddings.shape[1] if self.embeddings is not None else 0,
            "faiss_index_size": self.index.ntotal if self.index is not None else 0,
            "model_name": self.model_name
        }
        return stats