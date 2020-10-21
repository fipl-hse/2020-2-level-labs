"""
Tokenizer out of lab_1 for usage in lab_2
"""

import re


def tokenize(text: str) -> tuple:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    return tuple(re.findall('\w+', text.lower()))
