# ai_summary.py 
import re
from collections import Counter

def clean_text(text):
    """Clean text by removing extra spaces and newlines"""
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def generate_summary(text):
    # Clean text first
    text = clean_text(text)
    
    if len(text) < 100:
        return text[:200]
    
    # Rest of your existing code...
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    
    if len(sentences) <= 2:
        return sentences[0] if sentences else text[:200]
    
    # Find important words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
    
    words = text.lower().split()
    important_words = [w for w in words if w not in stop_words and len(w) > 3]
    word_freq = Counter(important_words)
    
    # Score sentences
    sentence_scores = {}
    for sent in sentences:
        score = sum(word_freq.get(word, 0) for word in sent.lower().split())
        sentence_scores[sent] = score
    
    # Get top 2 sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:2]
    summary = '. '.join([s[0] for s in top_sentences]) + '.'
    
    return summary[:500]
