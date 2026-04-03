from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile

from text_extractor import extract_from_pdf, extract_from_docx, extract_from_image
from ai_summary import generate_summary
from ai_entities import extract_entities
from ai_sentiment import analyze_sentiment

# Create FastAPI app
app = FastAPI(title="HCL Document Intelligence API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your API Key
VALID_API_KEYS = {"hcl_hackathon_2026"}

@app.post("/process")
async def process_document(
    file: UploadFile = File(...),
    api_key: str = Header(...)
):
    # 1. Validate API key
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # 2. Get filename
    filename = file.filename.lower()
    
    # 3. Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # 4. Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_from_pdf(tmp_path)
        elif filename.endswith('.docx'):
            text = extract_from_docx(tmp_path)
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            text = extract_from_image(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # 5. Check if text extracted
        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=422, detail="No readable text found")
        
        # 6. Apply AI
        summary = generate_summary(text)
        entities = extract_entities(text)
        sentiment = analyze_sentiment(text)
        
        # 7. Return response
        return {
            "filename": filename,
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
    print("\n" + "="*50)
    print("🚀 HCL Document Intelligence API (FastAPI)")
    print("="*50)
    print("📍 API URL: http://localhost:8000")
    print("🔑 API Key: hcl_hackathon_2026")
    print("📖 Interactive Docs: http://localhost:8000/docs")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)