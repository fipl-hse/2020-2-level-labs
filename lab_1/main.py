"""
Lab 1
A concordance extraction
"""

import re
def tokenize(text: str) -> list:
    pass
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s ]', '', text)
        text = text.split()
        return text
    else:
        return []

def remove_stop_words(tokens: list, stop_words: list) -> list:
    pass
    if isinstance(tokens, list):
        new_text = [word for word in tokens if word not in stop_words]
        return new_text
    else:
        return []

def calculate_frequencies(tokens: list) -> dict:
    pass

    if isinstance(tokens, list):
        for word in tokens:
            if isinstance(word, str):
                freq_dic = {word: tokens.count(word) for word in tokens}
                return freq_dic
            else:
                return {}
    else:
        return {}


def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    pass
    if (isinstance(freq_dict, dict) and isinstance(top_n, int)):
        list_of_items = list(freq_dict.items())
        list_of_items.sort(key=lambda x: x[1], reverse=True)
        top_n_words = []
        for pair_el in list_of_items:
            top_n_words.append(pair_el[0])
        return top_n_words[:top_n]
    else:
        return []


def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int) -> list:
    pass
    if not isinstance(tokens,list) or not isinstance(word,str) or (word not in tokens):
        return []
    if isinstance(left_context_size, bool) and isinstance(right_context_size, bool):
        return []
    if not isinstance(left_context_size, int) and not isinstance(right_context_size, int):
        return []
    if left_context_size < 1 and right_context_size < 1:
        return []
    concordance = []
    index_list = []
    for index, token in enumerate(tokens):
        if token == word:
            index_list.append(index)
    for ind in index_list:
        concordance.append(tokens[ind - left_context_size:ind + right_context_size + 1])
    return concordance

def get_adjacent_words(tokens: list, word: str, left_n: int, right_n: int) -> list:
    """
    Gets adjacent words from the left and right context
    :param tokens: a list of tokens
    :param word: a word-base for the search
    :param left_n: the distance between a word and an adjacent one in the left context
    :param right_n: the distance between a word and an adjacent one in the right context
    :return: a list of adjacent words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_n = 2
    right_n = 3
    --> [['man', 'is'], ['dog, 'cat']]
    """
    pass


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as fs:
        data = fs.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    pass


def sort_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int, left_sort: bool) -> list:
    """
    Gets a concordance of a word and sorts it by either left or right context
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :param left_sort: if True, sort by the left context, False – by the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    left_sort = True
    --> [['dog', 'is', 'happy', 'but', 'the', 'cat'], ['man', 'is', 'happy', 'the', 'dog', 'is']]
    """
    pass
