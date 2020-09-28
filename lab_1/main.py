"""
Lab 1
A concordance extraction
"""
from re import sub


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

    modified_text = text.lower()
    modified_text = sub(r'[^A-Za-z0-9\s]', '', modified_text)
    modified_text = modified_text.split()

    return modified_text


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
    if not isinstance(tokens, list):
        return []
    if not isinstance(stop_words, list):
        return tokens

    tokens_required = []
    for token in tokens:
        if token not in stop_words:
            tokens_required.append(token)

    return tokens_required


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if not isinstance(tokens, list):
        return {}
    for element in tokens:
        if not isinstance(element, str):
            return {}

    frequency_dictionary = {}
    for token in tokens:
        if token in frequency_dictionary.keys():
            frequency_dictionary[token] += 1
        else:
            frequency_dictionary[token] = 1

    return frequency_dictionary


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

    list_dictionary_items = list(freq_dict.items())
    list_dictionary_items.sort(key=lambda k_v: k_v[1], reverse=True)
    top_n_words = []
    if top_n > len(list_dictionary_items):
        top_n = len(list_dictionary_items)
    for index in range(top_n):
        top_n_words.append(list_dictionary_items[index][0])

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
    bool_left_size = isinstance(left_context_size, bool)
    bool_right_size = isinstance(right_context_size, bool)
    int_left_size = isinstance(left_context_size, int)
    int_right_size = isinstance(right_context_size, int)

    if (not isinstance(tokens, list)) or (not isinstance(word, str)) or (word not in tokens):
        return []
    if (bool_left_size and bool_right_size) or (not int_left_size and not int_right_size):
        return []

    bad_left_size = left_context_size < 1
    bad_right_size = right_context_size < 1
    if bad_left_size and bad_right_size:
        return []
    if (not int_left_size) or bad_left_size:
        left_context_size = 0
    elif (not int_right_size) or bad_right_size:
        right_context_size = 0

    concordance = []
    for index, token in enumerate(tokens):
        if token == word:
            if index < left_context_size:
                concordance += [tokens[:(index + right_context_size + 1)]]
            else:
                left_context = index - left_context_size
                right_context = index + right_context_size + 1
                concordance += [tokens[left_context:right_context]]

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
    tokens_is_list = isinstance(tokens, list)
    word_is_str = isinstance(word, str)
    bool_left_n = isinstance(left_n, bool)
    bool_right_n = isinstance(right_n, bool)
    int_left_n = isinstance(left_n, int)
    int_right_n = isinstance(right_n, int)

    if (not tokens_is_list) or (not word_is_str) or (word not in tokens):
        return []
    if (bool_left_n and bool_right_n) or (not int_left_n and not int_right_n):
        return []

    list_concordance = get_concordance(tokens, word, left_n, right_n)
    adjacent_words = []
    for context_list in list_concordance:
        for index, token in enumerate(context_list):
            if token == word:
                if len(context_list[:index]) < left_n:
                    if right_n < 1:
                        adjacent_words += [[context_list[0]]]
                    else:
                        adjacent_words += [[context_list[0], context_list[index + right_n]]]
                elif len(context_list[(index + 1):]) < right_n:
                    if left_n < 1:
                        adjacent_words += [[context_list[-1]]]
                    else:
                        adjacent_words += [[context_list[index - left_n], context_list[-1]]]
                elif (not isinstance(left_n, int)) or (left_n < 1):
                    adjacent_words += [[context_list[index + right_n]]]
                elif (not isinstance(right_n, int)) or (right_n < 1):
                    adjacent_words += [[context_list[index - left_n]]]
                else:
                    adjacent_words += [[context_list[index - left_n], context_list[index + right_n]]]

    return adjacent_words


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as opened_file:
        data = opened_file.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    context_list = []
    for word_list in content:
        word_context_str = ' '.join(word_list)
        context_list.append(word_context_str)
    all_context_str = '\n'.join(context_list)

    with open(path_to_file, 'w') as file_with_contexts:
        file_with_contexts.write(all_context_str)


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
    bool_left_sort = isinstance(left_sort, bool)
    bool_left_size = isinstance(left_context_size, bool)
    bool_right_size = isinstance(right_context_size, bool)
    int_left_size = isinstance(left_context_size, int)
    int_right_size = isinstance(right_context_size, int)

    if not bool_left_sort:
        return []
    if (bool_left_size and bool_right_size) or (not int_left_size and not int_right_size):
        return []
    if (left_context_size < 1 and left_sort) or (right_context_size < 1 and not left_sort):
        return []

    list_concordance = get_concordance(tokens, word, left_context_size, right_context_size)
    if left_sort:
        list_concordance.sort(key=lambda w: w[0])
    else:
        index_word = left_context_size + 1
        list_concordance.sort(key=lambda w: w[index_word])
    return list_concordance
