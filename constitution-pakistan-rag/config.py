# config.py
"""Simple configuration for Constitution RAG chatbot"""

import os

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "embeddings")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# Create directories if they don't exist
for directory in [DATA_DIR, EMBEDDINGS_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Document Processing
DEFAULT_PDF_PATH = os.path.join(BASE_DIR, "sample_constitution.txt")
CHUNK_MIN_LENGTH = 100

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "deepseek-coder:latest"
OLLAMA_TIMEOUT = 120

# Model Parameters
TEMPERATURE = 0.3
TOP_P = 0.9
MAX_TOKENS = 500

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"