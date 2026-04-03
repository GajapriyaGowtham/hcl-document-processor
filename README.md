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

```json
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




License
This project was created for the HCL Hackathon submission.
