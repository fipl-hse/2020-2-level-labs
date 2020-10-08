"""
Lab 1
A concordance extraction
"""
import re


def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lower cased tokens without punctuation
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
    if not isinstance(tokens, list) or not tokens or not isinstance(stop_words, list):
        return []

    while 'the' in tokens:
        tokens.remove('the')
    while 'is' in tokens:
        tokens.remove('is')
    tokens = [word for word in tokens if word not in stop_words]
    return list(tokens)


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """

    if isinstance(tokens, list):
        for word in tokens:
            if not isinstance(word, str):
                return {}
        cal_freq = {word: tokens.count(word) for word in tokens}
        return cal_freq
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

    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return []

    word_values = []
    for i in freq_dict.values():
        if i in word_values:
            continue
        word_values.append(i)
    word_values.sort()
    word_values = word_values[::-1]

    top = word_values[:top_n]
    top_n_words = []
    for element in top:
        for word, frequency in freq_dict.items():
            if element == frequency:
                top_n_words.append(word)
    top_n_words = top_n_words[:top_n]
    return top_n_words


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

    if isinstance(right_context_size, bool) or isinstance(left_context_size, bool):
        return []

    check = [isinstance(tokens, list), isinstance(word, str),
             isinstance(right_context_size, int), isinstance(left_context_size, int)]
    if not all(check):
        return []

    output_list = []
    inds = [ind for ind, w in enumerate(tokens) if w == word]

    if left_context_size > 0 and right_context_size > 0:
        output_list = [tokens[i - left_context_size:i + right_context_size + 1] for i in inds]
    elif left_context_size > 0 and not right_context_size > 0:
        output_list = [tokens[i - left_context_size:i + 1] for i in inds]
    elif right_context_size > 0 and not left_context_size > 0:
        output_list = [tokens[i:i + int(right_context_size) + 1] for i in inds]
    return output_list


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
    check = [isinstance(tokens, list),
             isinstance(word, str),
             isinstance(left_n, int),
             isinstance(right_n, int),
             not isinstance(left_n, bool),
             not isinstance(right_n, bool)]

    if not all(check):
        return []

    concordance = get_concordance(tokens, word, left_n, right_n)
    window = (left_n, right_n)

    if window[0] > 0 and window[1] > 0:
        return [[token[0], token[-1]]for token in concordance]
    if window[0] > 0:
        return [[token[0]] for token in concordance]
    if window[1] > 0:
        return [[token[-1]] for token in concordance]
    else:
        return []


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    if isinstance(path_to_file, str):
        return ' '

    with open('C:\\projects\2020-2-level-labs\\lab_1\\data.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """

    text = ''
    for i in content:
        value = ''.join(i)
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
