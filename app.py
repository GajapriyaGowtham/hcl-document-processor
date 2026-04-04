from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
import os
import tempfile
import base64
import re

from text_extractor import extract_from_pdf, extract_from_docx, extract_from_image
from ai_summary import generate_summary
from ai_entities import extract_entities
from ai_sentiment import analyze_sentiment

app = FastAPI(title="HCL Document Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_API_KEYS = {"hcl_hackathon_2026"}

@app.post("/process")
async def process_document(
    x_api_key: str = Header(..., alias="x-api-key"),
    file: Optional[UploadFile] = File(None),
    file_data: Optional[str] = Form(None),
    filename_from_form: Optional[str] = Form(None)
):
    # Validate API key
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # Handle file from different possible sources
    content = None
    filename = None
    
    # Case 1: File uploaded normally
    if file and file.filename:
        content = await file.read()
        filename = file.filename.lower()
    
    # Case 2: File sent as base64 string in form-data
    elif file_data:
        try:
            # Check if it's base64 encoded
            if ',' in file_data:
                file_data = file_data.split(',')[1]
            content = base64.b64decode(file_data)
            filename = filename_from_form or "uploaded_file.pdf"
        except:
            raise HTTPException(status_code=400, detail="Invalid file data format")
    
    else:
        raise HTTPException(status_code=400, detail="No file provided. Send as 'file' field or 'file_data' field")
    
    if not content or len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")
    
    filename = filename.lower()
    
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_from_pdf(tmp_path)
        elif filename.endswith('.docx'):
            text = extract_from_docx(tmp_path)
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            text = extract_from_image(tmp_path)
        elif filename.endswith('.txt'):
            with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        else:
            # Try OCR as fallback for any file
            text = extract_from_image(tmp_path)
        
        if not text or len(text.strip()) < 10:
            text = "Document contains minimal text. Unable to extract meaningful content."
        
        # AI Processing
        summary = generate_summary(text)
        entities = extract_entities(text)
        sentiment = analyze_sentiment(text)
        
        # Return response
        return {
            "fileName": filename,
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment["sentiment"],
            "sentiment_confidence": sentiment["confidence"],
            "word_count": len(text.split())
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.get("/")
async def root():
    return {
        "service": "HCL Document Intelligence",
        "version": "1.0",
        "api_key": "hcl_hackathon_2026",
        "endpoint": "POST /process",
        "docs": "/docs",
        "instructions": {
            "header": "x-api-key: hcl_hackathon_2026",
            "body": "form-data with key 'file' (multipart file upload)"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/test")
async def test():
    return {"message": "API is reachable", "status": "working"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
