# HCL Document Intelligence Processor

## Live URL
https://hcl-document-processor.onrender.com

## API Key
hcl_hackathon_2026

## API Endpoint
POST https://hcl-document-processor.onrender.com/process

## Headers
- x-api-key: hcl_hackathon_2026

## Body
- file: (PDF/DOCX/Image file)

## Response Format
```json
{
  "fileName": "document.pdf",
  "summary": "Concise summary of the document...",
  "entities": {
    "PERSON": ["Name"],
    "ORGANIZATION": ["Company"],
    "LOCATION": ["City"],
    "DATE": ["Date"],
    "MONEY": ["Amount"]
  },
  "sentiment": "positive/negative/neutral",
  "sentiment_confidence": 0.95,
  "word_count": 150
}
