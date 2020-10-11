"""
Tokenizer out of lab_1 for usage in lab_2
"""
import re


def tokenize(text: str) -> list:
    if not isinstance(text, str):
        return []

    text = text.lower()
    tokens = re.sub('[^a-z \n]', '', text)
    return tokens.split()
