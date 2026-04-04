from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile

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
    file: UploadFile = File(...),
    x_api_key: str = Header(..., alias="x-api-key")
):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    filename = file.filename.lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        if filename.endswith('.pdf'):
            text = extract_from_pdf(tmp_path)
        elif filename.endswith('.docx'):
            text = extract_from_docx(tmp_path)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            text = extract_from_image(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=422, detail="No readable text found")
        
        summary = generate_summary(text)
        entities = extract_entities(text)
        sentiment = analyze_sentiment(text)
        
        return {
            "fileName": filename,
            "summary": summary,
            "entities": entities,
            "sentiment": sentiment["sentiment"],
            "sentiment_confidence": sentiment["confidence"],
            "word_count": len(text.split())
        }
    
    finally:
        os.unlink(tmp_path)

@app.get("/")
async def root():
    return {
        "service": "HCL Document Intelligence",
        "version": "1.0",
        "api_key": "hcl_hackathon_2026",
        "endpoint": "POST /process",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
