"""
Tokenizer out of lab_1 for usage in lab_2
"""

'''def tokenize(text: str) -> list:
    if isinstance (text, str):
        clean_text_list = []
        raw_text_list = text.split()
        for word in raw_text_list:
            new_word = ''
            new_word2 = ''
            for sign in word:
                if sign.lower() in 'abcdefghijklmnopqrstuvwxyz ':
                    new_word += sign.lower()
                if sign == '.':
                    new_word2 = sign
            clean_text_list.append(new_word)
            clean_text_list.append(new_word2)
        for element in clean_text_list:
            if len(element) == 0:
                clean_text_list.pop(clean_text_list.index(element))
        clean_text_tuple = tuple(clean_text_list)
        return clean_text_tuple
    return []'''


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
    text_output = re.sub('[^a-z \n]', '', text.lower()).split('\n')
    return text_output
