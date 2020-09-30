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
        text = text.lower()
        tokens = re.sub('[\'\",.!0-9+=@#$%^&*()-_]+', '', text).split()
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

    new_li = []
    if isinstance(stop_words, list) and isinstance(tokens, list):
        for token in tokens:
            if token not in stop_words:
                new_li.append(token)
        return new_li

    if isinstance(tokens, list) and not isinstance(stop_words, list):
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
        for word in tokens:
            if not isinstance(word, str):
                freq_dict = {}

            elif word in freq_dict:
                freq_dict[word] += 1

            else:
                freq_dict[word] = 1

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
    """

    if isinstance(freq_dict, dict):
        sorted_d = sorted(freq_dict, key=freq_dict.get, reverse=True)[:top_n]
        return sorted_d

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

    concordance = []

    if_bool = isinstance(left_context_size, bool) or isinstance(right_context_size, bool)
    if_int = isinstance(left_context_size, int) or isinstance(right_context_size, int)

    if (not isinstance(tokens, list) or not if_int
            or not isinstance(word, str) or if_bool):
        return []
    for i, token in enumerate(tokens):
        if isinstance(token, str) and token == word:
            len_l = len(tokens[i - left_context_size:i])
            len_r = len(tokens[i: i + right_context_size + 1])
            left_w = tokens[i - left_context_size:i]
            right_w = tokens[i: i + right_context_size + 1]

            if ((1 <= left_context_size <= len_l)
                    and (1 <= right_context_size <= len_r)):
                context = left_w + right_w
                concordance.append(context)

            elif right_context_size < 1 <= left_context_size <= len_l:
                context = left_w
                concordance.append(context)

            elif left_context_size < 1 <= right_context_size:
                context = right_w
                concordance.append(context)

            elif (left_context_size > len_l) and (1 <= right_context_size <= len_r):
                context = tokens[0:i] + right_w
                concordance.append(context)

            elif (left_context_size > len_l) and (right_context_size < 1):
                context = tokens[0:i + 1]
                concordance.append(context)
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
    adj_w = []
    if_list_str = isinstance(tokens, list) and isinstance(word, str)
    if_int = isinstance(left_n, int) and isinstance(right_n, int)

    if (not if_list_str and not if_int
            and (right_n < 1) and (left_n < 1)):
        return []

    concordance = get_concordance(tokens, word, left_n, right_n)
    for cont in concordance:
        if left_n < 1 <= right_n:
            adj_w.append([cont[-1]])

        elif right_n < 1 <= left_n:
            adj_w.append([cont[0]])

        elif (right_n >= 1) and (left_n >= 1):
            adj_w.append([cont[0], cont[-1]])

    return adj_w


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
    text = ''
    for item in content:
        value = ' '.join(item)
        text += value + '\n'
    with open(path_to_file, 'w') as file:
        file.write(text)


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
