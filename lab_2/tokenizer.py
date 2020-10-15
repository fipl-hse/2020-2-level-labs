"""
Tokenizer out of lab_1 for usage in lab_2
"""
import re


def tokenize(text: str) -> tuple:
    if not isinstance(text, str):
        return ()

    tokens = []
    text = text.lower()
    if text[-1] == '.':
        text = text[:-1]  # a dot at the end of the text adds another empty list --> avoid this
    text = text.split('.')
    for sentence in text:
        sentence = re.sub(r'[^a-z\s]', '', sentence)
        tokens.append(tuple(sentence.split()))

    return tuple(tokens)
