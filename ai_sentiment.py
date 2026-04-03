# ai_sentiment.py
import re

def analyze_sentiment(text):
    if len(text) < 20:
        return {"sentiment": "neutral", "confidence": 0.5}
    
    text_lower = text.lower()
    
    # NEGATIVE words (for incidents, breaches, problems)
    negative_words = [
        'bad', 'terrible', 'awful', 'horrible', 'sad', 'negative', 
        'fail', 'failed', 'worst', 'hate', 'loss', 'decline', 
        'problem', 'error', 'breach', 'attack', 'hack', 'compromised',
        'data breach', 'cybersecurity', 'incident', 'exposed', 
        'vulnerability', 'threat', 'malware', 'ransomware',
        'critical', 'severe', 'urgent', 'warning', 'crisis'
    ]
    
    # POSITIVE words
    positive_words = [
        'good', 'great', 'excellent', 'amazing', 'happy', 'positive', 
        'success', 'successful', 'best', 'love', 'awesome', 
        'profit', 'growth', 'increase', 'gain', 'benefit'
    ]
    
    # Count occurrences
    neg_count = 0
    pos_count = 0
    
    for word in negative_words:
        neg_count += len(re.findall(r'\b' + word + r'\b', text_lower))
    
    for word in positive_words:
        pos_count += len(re.findall(r'\b' + word + r'\b', text_lower))
    
    # Determine sentiment
    if neg_count > pos_count:
        sentiment = "negative"
        confidence = min(0.95, neg_count / (neg_count + pos_count + 0.1))
    elif pos_count > neg_count:
        sentiment = "positive"
        confidence = min(0.95, pos_count / (pos_count + neg_count + 0.1))
    else:
        sentiment = "neutral"
        confidence = 0.5
    
    return {"sentiment": sentiment, "confidence": round(confidence, 2)}