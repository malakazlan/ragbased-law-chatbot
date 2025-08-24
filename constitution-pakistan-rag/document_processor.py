# document_processor.py
"""Simple document processor for PDF and text files"""

import re
import os
import fitz  # PyMuPDF
from config import DEFAULT_PDF_PATH, CHUNK_MIN_LENGTH

class DocumentProcessor:
    def __init__(self):
        """Initialize document processor"""
        self.text = ""
        self.chunks = []
        self.full_text = ""
    
    def load_document(self, file_path: str = None) -> str:
        """Load document from PDF or text file"""
        try:
            if file_path is None:
                file_path = DEFAULT_PDF_PATH
            
            if not os.path.exists(file_path):
                # Try to find a text file instead
                text_file = file_path.replace('.pdf', '.txt')
                if os.path.exists(text_file):
                    return self.load_text_file(text_file)
                else:
                    raise FileNotFoundError(f"Document file not found: {file_path}")
            
            # Check file extension
            if file_path.lower().endswith('.pdf'):
                return self.load_pdf(file_path)
            elif file_path.lower().endswith('.txt'):
                return self.load_text_file(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
                
        except Exception as e:
            print(f"❌ Error loading document: {e}")
            raise e
    
    def load_pdf(self, pdf_path: str) -> str:
        """Load and extract text from PDF file"""
        try:
            # Extract text from PDF
            doc = fitz.open(pdf_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            
            # Store the full text
            self.full_text = text
            self.text = text
            return text
            
        except Exception as e:
            print(f"❌ Error loading PDF: {e}")
            raise e
    
    def load_text_file(self, text_path: str) -> str:
        """Load text from text file"""
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Store the full text
            self.full_text = text
            self.text = text
            return text
            
        except Exception as e:
            print(f"❌ Error loading text file: {e}")
            raise e
    
    def chunk_document(self, text: str = None) -> list:
        """Split document into meaningful chunks"""
        if text is None:
            text = self.text
            
        if not text:
            raise ValueError("No text to chunk")
        
        # Split by Parts and Articles
        chunks = re.split(r'(PART\s+[IVXLCDM]+|Article\s+\d+[A-Z]?)', text)
        
        final_chunks = []
        for i in range(1, len(chunks), 2):
            heading = chunks[i].strip()
            body = chunks[i+1].strip() if i+1 < len(chunks) else ""
            
            if heading and body:
                chunk = f"{heading}\n{body}"
                if len(chunk.strip()) > CHUNK_MIN_LENGTH:
                    final_chunks.append(chunk)
        
        # Additional chunking for long sections
        processed_chunks = []
        for chunk in final_chunks:
            if len(chunk) > 2000:  # Split very long chunks
                sub_chunks = self._split_long_chunk(chunk)
                processed_chunks.extend(sub_chunks)
            else:
                processed_chunks.append(chunk)
        
        self.chunks = processed_chunks
        return processed_chunks
    
    def _split_long_chunk(self, chunk: str, max_length: int = 1500) -> list:
        """Split long chunks into smaller pieces"""
        lines = chunk.split('\n')
        current_chunk = ""
        chunks = []
        
        for line in lines:
            if len(current_chunk) + len(line) > max_length and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = line + "\n"
            else:
                current_chunk += line + "\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def get_chunk_stats(self) -> dict:
        """Get statistics about the processed chunks"""
        if not hasattr(self, 'chunks') or not self.chunks:
            return {"total_chunks": 0, "avg_chunk_length": 0, "total_text_length": 0}
        
        total_chunks = len(self.chunks)
        total_length = sum(len(chunk) for chunk in self.chunks)
        avg_length = total_length / total_chunks if total_chunks > 0 else 0
        
        return {
            "total_chunks": total_chunks,
            "avg_chunk_length": round(avg_length, 2),
            "total_text_length": total_length
        }
    
    def get_full_text(self) -> str:
        """Get the full processed text"""
        return self.full_text if hasattr(self, 'full_text') else ""
    
    def get_chunks(self) -> list:
        """Get the processed chunks"""
        return self.chunks if hasattr(self, 'chunks') else []