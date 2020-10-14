"""
Tokenizer out of lab_1 for usage in lab_2
"""
def tokenize_by_lines(text: str) -> tuple:
    if not isinstance(text, str):
        return []
    tokens = []
    for token in text.lower().split():
        variable = ''
        for character in token:
            if character.isalpha():
                variable += character
        if len(variable) != 0:
            tokens.append(variable)
    return tokens


