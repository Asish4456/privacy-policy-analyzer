import re

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_sentences(text):
    return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
