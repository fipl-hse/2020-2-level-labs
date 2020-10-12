"""
Tokenizer out of lab_1 for usage in lab_2
"""
text = '''I have a cat.\nHis name is Bruno.\nBruno's best friend is Richard.'''
print(text)


def tokenize(text: str) -> tuple:
    if isinstance(text, str):
        text = text.lower()
        tokens = re.sub('[\'\",.!0-9+=@#$%^&*()-_]+', '', text)
        # return tokens
    print(tokens)
