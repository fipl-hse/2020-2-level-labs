"""
Lab 1
A concordance extraction
"""

import re

def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    if isinstance(text, str):
        tokens = re.sub(r'[^\w\s]', '', text.lower())
        tokens = tokens.split()
        return tokens
    return []


def remove_stop_words(tokens: list, stop_words: list) -> list:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    stop_words = ['the', 'is']
    --> ['weather', 'sunny', 'man', 'happy']
    """
    if isinstance(tokens, list):
        if isinstance(stop_words, list):
            tokens = [token for token in tokens if token not in stop_words]
            return tokens
        return tokens
    return []


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    freq_dict = {}
    if isinstance(tokens, list):
        for token in tokens:
            if isinstance(token, str):
                freq_dict[token] = tokens.count(token)
            else:
                return {}
        return freq_dict
    return {}


def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words to return
    :return: a list of the most common words
    e.g. tokens = ['weather', 'sunny', 'man', 'happy', 'and', 'dog', 'happy']
    top_n = 1
    --> ['happy']
    Здесь при неккорректных значениях должен возвращаться пустой список!
    """
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        sorted_dict = sorted(freq_dict, key=freq_dict.get, reverse=True)
        top_n_words = sorted_dict[:top_n]
        return top_n_words
    return []


def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int) -> list:
    """
    Gets a concordance of a word
    A concordance is a listing of each occurrence of a word in a text,
    presented with the words surrounding it
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    --> [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]
    """
    checking = [isinstance(tokens, list), isinstance(word, str), isinstance(left_context_size, int),
                not isinstance(left_context_size, bool), isinstance(right_context_size, int),
                not isinstance(right_context_size, bool)]

    if all(checking) == False:
        return []

    concordance = []
    indexes = [i for i, x in enumerate(tokens) if x == word]

    if left_context_size > 0 and right_context_size > 0:
        concordance += [tokens[i - left_context_size: i + right_context_size + 1] for i in indexes]
    elif left_context_size > 0:
        concordance += [tokens[i - left_context_size: i + 1] for i in indexes]
    elif right_context_size > 0:
        concordance += [tokens[i: i + right_context_size + 1] for i in indexes]
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
    В данной функции ОБЯЗАТЕЛЬНО использовать функцию get_concordance (см. Шаг 5).
    """
    if not isinstance(tokens, list) or not isinstance(word, str):
        return []

    if type(left_n) != int and type (right_n) != int:
        return []
    if left_n < 0 or right_n < 0:
        return []

    adjacent_words = []

    for i in get_concordance(tokens, word, left_n, right_n):
        if left_n > 0 and right_n > 0:
            adjacent_words += [[i[0], i[-1]]]
        elif left_n > 0:
            adjacent_words += [[i[0]]]
        elif right_n > 0:
            adjacent_words += [[i[-1]]]
    return adjacent_words


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as file:
        data = file.read()
    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    if isinstance(path_to_file, str) and isinstance(content, list):
        result = [' '.join(i) for i in content]
        with open(path_to_file, 'w') as file:
            file.write('\n'.join(result))


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
    В данной функции ОБЯЗАТЕЛЬНО использовать функцию get_concordance (см. Шаг 5).
    """
    concordance = []

    if isinstance(left_sort, bool) and isinstance(left_context_size, int) and isinstance(right_context_size, int):
        if left_sort > 0 and left_context_size > 0:
            concordance = sorted(get_concordance(tokens, word, left_context_size, right_context_size))
        elif left_sort <= 0 and right_context_size <= 0:
            return []
        elif right_context_size > 0 >= left_sort:
            concordance = sorted(get_concordance(tokens, word, left_context_size, right_context_size),
                                 key=lambda words: words[left_context_size + 1])
    else:
        return []

    return concordance
