# HCL Document Intelligence Processor

AI-powered document processing system that extracts, analyzes, and summarizes content from PDF, DOCX, and Image files.

## Live URL
https://hcl-document-processor.onrender.com

## API Key
hcl_hackathon_2026

## API Endpoint
POST https://hcl-document-processor.onrender.com/process

## Headers
| Header | Value |
|--------|-------|
| x-api-key | hcl_hackathon_2026 |

## Request Body
| Key | Type | Value |
|-----|------|-------|
| file | file | PDF/DOCX/Image file |

## Response Format
{
"fileName": "document.pdf",
"summary": "Concise summary of the document...",
"entities": {
"PERSON": ["John Doe"],
"ORGANIZATION": ["HCL Technologies"],
"LOCATION": ["New York"],
"DATE": ["January 2024"],
"MONEY": ["$10,000"]
},
"sentiment": "positive",
"sentiment_confidence": 0.95,
"word_count": 150
}


## AI Tools Used

- **spaCy (en_core_web_sm)** - Named Entity Recognition
- **Tesseract OCR** - Text extraction from images
- **Custom algorithms** - Summarization using sentence scoring
- **Custom algorithms** - Sentiment analysis using keyword matching

## Tech Stack

- **FastAPI** - Web framework
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX text extraction
- **Pillow + Tesseract** - Image OCR
- **spaCy** - NLP processing
- **Render** - Cloud hosting with Docker

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Tesseract OCR installed

### Installation
git clone https://github.com/GajapriyaGowtham/hcl-document-processor.git
cd hcl-document-processor
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py


### Windows Tesseract OCR
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Supported Formats

| Format | Extension |
|--------|-----------|
| PDF | .pdf |
| Word Document | .docx |
| Images | .png, .jpg, .jpeg |

## How to Test

### Using Python
import requests

url = "https://hcl-document-processor.onrender.com/process"
headers = {"x-api-key": "hcl_hackathon_2026"}

with open("document.pdf", "rb") as f:
files = {"file": f}
response = requests.post(url, headers=headers, files=files)
print(response.json())

### Using cURL
curl -X POST https://hcl-document-processor.onrender.com/process
-H "x-api-key: hcl_hackathon_2026"
-F "file=@document.pdf"

### Using API Docs
Open browser: https://hcl-document-processor.onrender.com/docs

## Architecture
Upload File → FastAPI → Text Extractor → AI Processing → JSON Response
↓ ↓ ↓
API Key Auth PDF/DOCX/OCR Summarization
Entity Extraction
Sentiment Analysis

## Features

- ✅ Multi-format support (PDF, DOCX, Images)
- ✅ Automatic text extraction with OCR
- ✅ AI-powered summarization
- ✅ Named entity extraction (People, Organizations, Locations, Dates, Money)
- ✅ Sentiment analysis (Positive/Negative/Neutral)
- ✅ API key authentication
- ✅ Auto-generated API documentation

## Known Limitations

- Maximum file size: 10MB
- OCR works best with clear, printed text
- First request may take 10-15 seconds (model loading)
- Free Render tier may spin down after 15 minutes of inactivity
- Limited to English language text

## File Structure
hcl-document-processor/
├── app.py # Main FastAPI server
├── text_extractor.py # PDF/DOCX/Image extraction
├── ai_summary.py # Summarization logic
├── ai_entities.py # Entity extraction (spaCy)
├── ai_sentiment.py # Sentiment analysis
├── requirements.txt # Python dependencies
├── Dockerfile # Container configuration
└── README.md # Documentation

## Submission Details

- **Hackathon:** HCL Hackathon 2026
- **Category:** AI-Powered Document Analysis & Extraction
- **Author:** Gajapriya Gowtham

## License

This project was created for the HCL Hackathon submission.
