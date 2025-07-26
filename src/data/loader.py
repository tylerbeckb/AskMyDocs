from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from typing import List
from langchain_core.documents import Document

class DocumentLoader:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def load_pdf(self, file_path: str) -> List[Document]:
      """Load a PDF file and split it into chunks"""
      # Check if the file exists
      if not os.path.exists(file_path):
          raise FileNotFoundError(f"PDF file not found: {file_path}")
      
      try:
          # Load the PDF file using PyPDFLoader
          loader = PyPDFLoader(file_path)
          # Load the documents from the PDF
          docs = loader.load()
          # Split the documents into chunks
          chunks = self.text_splitter.split_documents(docs)
          return chunks
      except Exception as e:
          raise RuntimeError(f"Failed to load PDF file: {file_path}. Error: {str(e)}")