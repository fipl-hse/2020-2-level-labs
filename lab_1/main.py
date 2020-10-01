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
    tokens = []
    if text and isinstance(text, str):
        tokens = re.sub('[^a-z \n]', '', text.lower()).split()
    return tokens


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
    if isinstance(tokens, list) and isinstance(stop_words, list):
        for word in tokens:
            if not isinstance(word, str):
                return []

        tokens = [word for word in tokens if word not in stop_words]
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
        for k in tokens:
            if not isinstance(k, str):
                freq_dict = {}
            elif k in freq_dict:
                freq_dict[k] += 1
            else:
                freq_dict[k] = 1
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
    if (not isinstance(freq_dict, dict)) or (not isinstance(top_n, int)):
        return []

    sorted_dict = dict(
        sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))  # упорядочим элементы словаря по значениям
    sorted_dict = list(sorted_dict.keys())

    if top_n >= 0:
        common_words = sorted_dict[:top_n]
    else:
        common_words = []

    return common_words


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

    lcs = left_context_size
    rcs = right_context_size
    it_bool = isinstance(lcs, bool) or isinstance(rcs, bool)
    it_int = isinstance(lcs, int) or isinstance(rcs, int)

    if not isinstance(tokens, list) or not isinstance(word, str):
        return []
    if it_bool or (not it_int) or (lcs < 1 and rcs < 1):
        return []

    if lcs < 0:
        lcs = 0
    elif rcs < 0:
        rcs = 0
    for index, token in enumerate(tokens):
        if token == word:
            concordance.append(tokens[index - lcs: index + rcs + 1])
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
    if not isinstance(tokens, list) or not isinstance(word, str) \
            or not isinstance(left_n, int) or not isinstance(right_n, int):
        return []

    func_tokens = get_concordance(tokens, word, left_n, right_n)
    adj_words_list = []

    if all(func_tokens):
        for i in get_concordance(tokens, word, left_n, right_n):
            if left_n > 0 and right_n > 0:
                adj_words_list.append([i[0], i[-1]])
            elif left_n > 0:
                adj_words_list.append([i[0]])
            elif right_n > 0:
                adj_words_list.append([i[-1]])

    return adj_words_list


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
    output_file = [' '.join(i) for i in content]

    with open(path_to_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(output_file))


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
    if not isinstance(left_sort, bool) or not isinstance(tokens, list) or not isinstance(word, str) \
            or not isinstance(left_context_size, int) or not isinstance(right_context_size, int):
        return []

    concord = get_concordance(tokens, word, left_context_size, right_context_size)
    if left_sort and left_context_size > 0:
        return sorted(concord)
    if not left_sort and right_context_size > 0:
        return sorted(concord, key=lambda element: element[element.index(word) + 1])
    return []
