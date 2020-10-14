"""
Tokenizer out of lab_1 for usage in lab_2
"""

def tokenize(text: str) -> tuple:
    tokens = ''
    all_sent = []
    text = text.lower()
    for i in text:
        if i.isalpha() or i == ' ' or i == '\n':
            tokens += i
    tokens = tokens.split('\n')
    for el in tokens:
        all_tokens = tuple(el.split(' '))
        all_sent.append(all_tokens)
    all_sent = tuple(all_sent)
    return all_sent

