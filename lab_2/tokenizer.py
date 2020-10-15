"""
Tokenizer out of lab_1 for usage in lab_2
"""
text = '''I have a cat.\nHis name is Bruno.\nBruno's best friend is Richard.\Ricard's owner is one of 
the best friends of my parents\nMy parents have a cat too'''
import re
def tokenize(text: str) -> tuple:
    if isinstance(text, str):
        text = text.lower()
        tokens = re.sub('[\'\",.!0-9+=@#$%^&*()-_]+', '', text)
        tokens = re.split('\\n', tokens)
        all_t = []
        for t in tokens:
            t = t.split()
            t = tuple(t)
            all_t.append(t)
        all_t = tuple(all_t)
        print(all_t) # return
tokenize(text)
