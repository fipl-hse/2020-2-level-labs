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

import re


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
