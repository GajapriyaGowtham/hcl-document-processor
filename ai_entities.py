# ai_entities.py
import spacy
import re

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """Clean text by removing extra spaces and newlines"""
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_entities(text):
    """Extract named entities from text"""
    if len(text) < 10:
        return {}
    
    # Clean the text first
    clean_text_content = clean_text(text)
    
    # Process text (limit for speed)
    doc = nlp(clean_text_content[:5000])
    
    entities = {
        "PERSON": [],
        "ORGANIZATION": [],
        "LOCATION": [],
        "DATE": [],
        "MONEY": []
    }
    
    # Common words to filter out (not real entities)
    filter_words = [
        'cybersecurity incident report', 'major data breach', 'financial institutions',
        'the', 'a', 'an', 'this', 'that', 'these', 'those', 'it', 'they', 'we', 'you'
    ]
    
    for ent in doc.ents:
        entity_value = clean_text(ent.text)
        entity_lower = entity_value.lower()
        
        # Skip if it's a filtered word or too short
        if len(entity_value) < 3:
            continue
        if entity_lower in filter_words:
            continue
        if len(entity_value) > 50:  # Skip very long matches
            continue
        
        if ent.label_ == "PERSON" and entity_value not in entities["PERSON"]:
            # Skip if it looks like a title
            if not entity_value.endswith(('Report', 'Breach', 'Affects')):
                entities["PERSON"].append(entity_value)
                
        elif ent.label_ == "ORG" and entity_value not in entities["ORGANIZATION"]:
            # Skip if it contains report/breach keywords
            if not any(word in entity_lower for word in ['report', 'breach', 'incident', 'analysis']):
                entities["ORGANIZATION"].append(entity_value)
                
        elif ent.label_ in ["GPE", "LOC"] and entity_value not in entities["LOCATION"]:
            entities["LOCATION"].append(entity_value)
            
        elif ent.label_ == "DATE" and entity_value not in entities["DATE"]:
            entities["DATE"].append(entity_value)
            
        elif ent.label_ == "MONEY" and entity_value not in entities["MONEY"]:
            entities["MONEY"].append(entity_value)
    
    # Also find organizations using pattern matching
    org_pattern = r'\b([A-Z][a-z]+ (?:Bank|Corp|Inc|LLC|Financial|Institution|Company))\b'
    org_matches = re.findall(org_pattern, clean_text_content)
    for org in org_matches[:5]:
        if org not in entities["ORGANIZATION"]:
            entities["ORGANIZATION"].append(org)
    
    # Find money amounts
    money_pattern = r'\$\s?\d+(?:,\d+)*(?:\.\d+)?|\d+\s?(?:million|billion|dollars)'
    money_matches = re.findall(money_pattern, clean_text_content, re.IGNORECASE)
    for money in money_matches[:3]:
        if money not in entities["MONEY"]:
            entities["MONEY"].append(money)
    
    # Remove empty lists
    return {k: v for k, v in entities.items() if v}