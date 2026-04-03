# text_extractor.py
# This file handles reading text from PDF, DOCX, and Images

import PyPDF2
from docx import Document
from PIL import Image
import pytesseract
import os

def extract_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PDF error: {e}")
    return text if text.strip() else "No text found"

def extract_from_docx(file_path):
    """Extract text from DOCX file"""
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"
    except Exception as e:
        print(f"DOCX error: {e}")
    return text if text.strip() else "No text found"

def extract_from_image(file_path):
    """Extract text from image using OCR"""
    try:
        # Set Tesseract path for Windows
        tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        ]
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
        
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip() if text.strip() else "No text found"
    except Exception as e:
        print(f"Image error: {e}")
        return "Error reading image"