import fitz 
import re
from typing import Dict, List, Any

class PDFParser:
    def __init__(self):
        self.doc = None
        self.file_path = None
    
    def open(self, file_path: str) -> bool:
        """Open a PDF file for parsing"""
        try:
            self.file_path = file_path
            self.doc = fitz.open(file_path)
            return True
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return False
        
    def extract_all_text(self) -> str:
        """Extract all text from the PDF"""
        if not self.doc:
            return ""
        
        text = ""
        for page in self.doc:
            text += page.get_text()
        return text
    
    def extract_text_by_page(self) -> List[str]:
        """Extract text from each page as a list"""
        if not self.doc:
            return []
        return [page.get_text() for page in self.doc]
    
    def extract_metadata(self) -> Dict[str, Any]:
        """Extract document metadata"""
        if not self.doc:
            return {}
        return self.doc.metadata
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text - remove headers, footers, page numbers"""
        # Remove page numbers
        cleaned = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        # Remove headers/footers (customize for your specific documents)
        cleaned = re.sub(r'Travel Insurance Policy\s*\|.*?\n', '', cleaned)
        # Remove repeated whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()
    
    def close(self):
        """Close the PDF document"""
        if self.doc:
            self.doc.close()
            self.doc = None
            self.file_path = None
        else:
            print("No document is currently open.")
    