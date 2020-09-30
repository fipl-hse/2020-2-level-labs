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
    new_text = ''

    if not isinstance(text, str):
        return []

    for elem in text:
        if elem.isalpha() or re.fullmatch('[\s]', elem):
            new_text += elem
    new_text = new_text.lower().split()

    return new_text


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

    new_list = [word for word in tokens if word not in stop_words]
    return new_list


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

    dic = {words: tokens.count(words) for words in tokens if isinstance(words, str)}
    return dic


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

    list_of_values = []

    for value in freq_dict.values():
        if value not in list_of_values:
            list_of_values += [value]
    list_of_values = sorted(list_of_values, reverse=True)

    top_words = []

    for value in list_of_values:
        similar_freq_words = []

        for keys in freq_dict:
            if freq_dict[keys] == value:
                similar_freq_words.append(keys)
        top_words.extend(similar_freq_words)

    if top_n <= len(top_words):
        return top_words[:top_n]
    else:
        return top_words


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
    if isinstance(left_context_size, bool) or isinstance(right_context_size, bool):
        return []

    if (not isinstance(tokens, list) or not isinstance(word, str) or not isinstance(left_context_size, int)
            or not isinstance(right_context_size, int) or (left_context_size < 1 and right_context_size < 1)):
        return []

    main_indexes = []
    concordance = []

    for idx, elem in enumerate(tokens):
        if elem == word:
            main_indexes += [idx]

    for indexes in main_indexes:
        if left_context_size < 1 and len(tokens) - indexes - 1 > right_context_size:
            concordance.append([tokens[indexes:indexes + right_context_size + 1]])

        elif left_context_size < 1 and len(tokens) - indexes - 1 <= right_context_size:
            concordance.append(tokens[indexes:])

        else:
            concordance.append(tokens[indexes - left_context_size: indexes + 1 + right_context_size])

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
    context_line = get_concordance(tokens, word, left_n, right_n)
    adjacent_words = []

    for element in context_line:
        if left_n == 0:
            adjacent_words.extend([[element[-1]]])

        elif right_n == 0:
            adjacent_words.extend([[element[0]]])

        else:
            adjacent_words.extend([[element[0], element[-1]]])

    return adjacent_words


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
    if isinstance(path_to_file, str) and isinstance(content, list):

        with open(path_to_file, 'w', encoding='utf-8') as file:
            for concordance in content:
                file.write(' '.join(concordance) + '\n')


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
    if (not isinstance(left_context_size, int) or not isinstance(right_context_size, int)
            or not isinstance(left_sort, bool)):
        return []

    concordance = get_concordance(tokens, word, left_context_size, right_context_size)

    if left_sort and left_context_size > 0:
        concordance.sort()

    elif not left_sort and right_context_size > 0:
        concordance.sort(key=lambda elem: elem[elem.index(word) + 1])

    else:
        concordance = []

    return concordance
