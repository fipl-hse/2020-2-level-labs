"""
Tokenizer out of lab_1 for usage in lab_2
"""
def tokenize(text: str) -> tuple:
    if not isinstance(text, str):
        return ()
    text = text.lower()
    for symbol in text:
        if symbol.isalpha() is False and symbol != ' ' and symbol != '\n':
            text = text.replace(symbol, '')
        elif symbol == '\n':
            text = text.replace(symbol, ' ')
    tokens = text.split()
    return sentences_tuple

