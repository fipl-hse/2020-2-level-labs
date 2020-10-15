"""
Tokenizer out of lab_1 for usage in lab_2
"""
import re

import re

<<<<<<< HEAD
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
=======

def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    if not isinstance(text, str):
        return []
    text_output = re.sub('[^a-z \n]', '', text.lower()).split()
    return text_output
>>>>>>> a977c486117a69202aa048031508d37068dedbc9
