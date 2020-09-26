"""
Lab 1
A concordance extraction
"""


def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """

    import re
    from string import punctuation

    if type(text) is str:
        text = re.sub(f'[{punctuation}]+', '', text.lower())
        text = re.findall(r'\w+', text)
        return text
    else:
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

    if type(tokens) is list:
        return [x for x in tokens if x not in set(stop_words)]
    else:
        return []


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """

    if type(tokens) is list and all(tokens):
        return {token: tokens.count(token) for token in tokens}
    else:
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

    if type(freq_dict) is dict:
        sorted_dict = [k for k, _ in sorted(freq_dict.items(), key=lambda kv: kv[1], reverse=True)]
        return sorted_dict[:top_n]
    else:
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

    checks = [
        type(tokens) is list,
        type(word) is str,
        type(left_context_size) is int,
        type(right_context_size) is int
    ]

    if all(checks):
        context = []
        word_indices = [idx for idx, el in enumerate(tokens) if el == word]
        window = (left_context_size, right_context_size)

        for x in word_indices:
            if window[0] > 0 and window[1] > 0:
                context.append(tokens[x - window[0]:x + window[1] + 1])
            elif window[1] > 0:
                context.append(tokens[x:x + window[1] + 1])
            elif window[0] > 0:
                context.append(tokens[x - window[0]:x + 1])
            else:
                return []
        return context

    else:
        return []


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

    checks = [
        type(tokens) is list,
        type(word) is str,
        type(left_n) is int,
        type(right_n) is int
    ]

    if all(checks):
        window = (left_n, right_n)
        concordance = get_concordance(tokens, word, left_n, right_n)

        if window[0] > 0 and window[1] > 0:
            return [[token[0], token[-1]] for token in concordance]
        elif window[1] > 0:
            return [[token[-1]] for token in concordance]
        elif window[0] > 0:
            return [[token[0]] for token in concordance]
        else:
            return []

    else:
        return []


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

    with open(path_to_file, 'w', encoding='utf-8') as data:
        for i in content:
            data.write(f'{repr(i)}\n')


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

    checks = [
        type(tokens) is list,
        type(word) is str,
        type(left_context_size) is int,
        type(right_context_size) is int,
        type(left_sort) is bool
    ]

    if all(checks):
        concordance = get_concordance(tokens, word, left_context_size, right_context_size)
        window = (left_context_size, right_context_size)

        if left_sort and window[0] > 0:
            return sorted(concordance)
        elif not left_sort and window[1] > 0:
            return sorted(concordance, key=lambda x: x[x.index(word) + 1])
        else:
            return []
    else:
        return []
