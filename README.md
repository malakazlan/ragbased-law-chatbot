# 🇵🇰 Constitution of Pakistan RAG Chatbot

A **simple, powerful, and reliable** RAG (Retrieval-Augmented Generation) chatbot that answers questions about Pakistan's Constitution using intelligent text search and smart fallback responses.

## ✨ Features

- **🔍 Smart Search**: FAISS vector search finds relevant constitutional sections
- **📚 Source Display**: See exactly what constitutional text was used
- **🤖 Intelligent Answers**: Smart fallback system provides accurate responses
- **⚡ Fast & Reliable**: No AI model failures or timeouts
- **🎯 Simple Interface**: Clean Streamlit UI for easy interaction

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Chatbot
```bash
streamlit run constitution-pakistan-rag/main.py
```

### 3. Open Your Browser
Navigate to: `http://localhost:8501`

### 4. Start Chatting!
- Click "Initialize System" in the sidebar
- Ask questions about Pakistan's Constitution
- Get instant answers with source references

## 💡 Example Questions

- "What is the state religion of Pakistan?"
- "What are fundamental rights?"
- "How is the Prime Minister appointed?"
- "What is the structure of Parliament?"
- "What are the powers of the Supreme Court?"

## 🏗️ Architecture

```
📄 Constitution Text → 🔍 FAISS Search → 📚 Relevant Sections → 💬 Smart Answer
```

### Core Components

- **`main.py`**: Streamlit application entry point
- **`chat_interface.py`**: User interface and chat logic
- **`rag_system.py`**: Main RAG orchestration
- **`embedding_manager.py`**: FAISS vector search and embeddings
- **`document_processor.py`**: Text processing and chunking
- **`ollama_client.py`**: Smart fallback response system
- **`config.py`**: Configuration settings

## 🔧 How It Works

1. **Document Loading**: Loads Constitution text and creates chunks
2. **Embedding Creation**: Generates vector embeddings using sentence-transformers
3. **Smart Search**: FAISS finds most relevant constitutional sections
4. **Answer Generation**: Smart fallback system provides accurate responses
5. **Source Display**: Shows exactly what text was used

## 📁 Project Structure

```
constitution-pakistan-rag/
├── main.py                 # Main Streamlit app
├── chat_interface.py       # Chat UI and logic
├── rag_system.py          # RAG system core
├── embedding_manager.py    # FAISS search & embeddings
├── document_processor.py   # Text processing
├── ollama_client.py       # Smart fallback system
├── config.py              # Configuration
└── sample_constitution.txt # Constitution text data
```

## 🎯 Why This Approach?

- **✅ Always Works**: No AI model failures or timeouts
- **✅ Accurate Answers**: Based directly on constitutional text
- **✅ Source Transparency**: See exactly what was used
- **✅ Fast Responses**: No waiting for AI generation
- **✅ Simple & Reliable**: Clean, maintainable code

## 🛠️ Requirements

- Python 3.8+
- Streamlit
- FAISS
- Sentence Transformers
- PyMuPDF (for PDF support)

## 🔄 Updates

- **Simplified Architecture**: Removed unnecessary complexity
- **Smart Fallback**: Intelligent responses without AI model dependency
- **Clean Code**: Focused on core RAG functionality
- **Reliable Performance**: Consistent, fast responses

##  Support

This chatbot provides **professional-grade constitutional assistance** with:
- Instant answers
- Source verification
- Reliable performance
- Clean interface


**Perfect for legal professionals, students, and anyone interested in Pakistan's Constitution!** 🎉
