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
    if not isinstance(text, str):
        return []
    text = text.lower()
    text = re.sub("[^A-Za-z ]", "", text)
    tokens = text.split()
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

    if not isinstance(text, str):
        return []
    if not isinstance(stop_words, list):
        return tokens
    tokens_new = [i for i in tokens if i not in stop_words]
    return (tokens_new)

    pass



def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """

    if not isinstance(tokens, list) and not all(isinstance(c, str) for c in tokens):
        return {}
    freq_dict = {a: tokens.count(a) for a in tokens}
    return freq_dict
    pass


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
    freq_dict = {a: tokens.count(a) for a in tokens}
    if not isinstance(freq_dict, dict) and not all(isinstance(c, str) for c in tokens) and not top_n >= 0:
        return {}
    list_words = sorted(freq_dict, key=freq_dict.get, reverse=True)
    return (list_words[:top_n])
    pass


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
    check_left = isinstance(left_context_size, int) and not isinstance(left_context_size, bool)
    check_right = isinstance(right_context_size, int) and not isinstance(right_context_size, bool)
    if not isinstance(tokens, list) or not isinstance(word, str) or not word.isalpha():
        return []
    if not check_left or not check_right or (left_context_size < 1 and right_context_size < 1):
        return []
    if not isinstance(tokens, list) or not isinstance(word, str):
        return []
    if left_context_size < 0:
        left_context_size = 0
    elif right_context_size < 0:
        right_context_size = 0
    conc = []
    for i, c in enumerate(tokens):
        if c == word:
            conc.append(tokens[i - left_context_size: i + right_context_size + 1])
    return conc
    pass


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
    if not isinstance(tokens, list) and not isinstance(word, str):
        return []
    elif not isinstance(left_n, int) and not isinstance(right_n, int):
        return []
    conc_1 = get_concordance(tokens, word, left_n, right_n)
    couples_list = []
    for i in conc_1:
        if right_n <= 0:
            couples_list.append([i[0]])
        elif left_n <= 0:
            couples_list.append([i[-1]])
        else:
            couples_list.append([i[0], i[-1]])
    return couples_list

    pass


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
    for i in content:
        text_1 = " ".join(i)
    with open(path_to_file, 'w') as file:
        file.write("\n".join(text_1))
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
    conc = get_concordance(tokens, word, left_context_size, right_context_size)
    if conc == [] or not isinstance(left_sort, bool):
        return []
    if left_sort:
        if left_context_size <= 0:
            return []
        word_index = 0
    else:
        if right_context_size <= 0:
            return []
        word_index = conc[0].index(word) + 1
    sorted_conc = []
    words_list = [i[word_index] for i in conc]
    for i in sorted(words_list):
        for context in conc:
            if i == context[word_index]:
                sorted_conc.append(context)
                conc.remove(context)
                break
    return sorted_conc

    pass
