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
    if isinstance(text, str) and text:
        prepared_text = re.sub('[^a-zA-Z \n`]', '', text).lower()
        return prepared_text.split()

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
    if isinstance(tokens, list) and tokens and isinstance(stop_words, list) and stop_words:
        output_list = tokens[:]

        for word in tokens:
            if word in stop_words:
                output_list.remove(word)

        return output_list

    elif (isinstance(tokens, list) and tokens) and not (isinstance(stop_words, list) and stop_words):
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
    if isinstance(tokens, list) and tokens:
        for word in tokens:
            if not isinstance(word, str):
                return {}

        return {word: tokens.count(word) for word in tokens}

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
    if isinstance(freq_dict, dict) and isinstance(top_n, int) and freq_dict and top_n >= 1:
        items_list = list(freq_dict.items())

        values_dict = {}
        for pair in items_list:
            if pair[1] in values_dict.keys():
                values_dict[pair[1]].append(pair[0])
            else:
                values_dict[int(pair[1])] = [pair[0]]

        top_n_list = list(values_dict.keys())
        top_n_list.sort()

        output_top = []
        for ind in top_n_list:
            output_top.extend(values_dict[ind][::-1])

        output_top.reverse()
        return output_top[:top_n]

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
    if isinstance(right_context_size, bool) and isinstance(left_context_size, bool):
        return []
    elif isinstance(tokens, list) and isinstance(word, str) and isinstance(right_context_size, int) and isinstance(
            left_context_size, int):

        inds = [ind for ind, w in enumerate(tokens) if w == word]

        if left_context_size > 0 and right_context_size > 0:
            output_list = [tokens[i - left_context_size:i + right_context_size + 1] for i in inds]

        elif left_context_size > 0:
            output_list = [tokens[i - left_context_size:i + 1] for i in inds]

        elif right_context_size > 0:
            output_list = [tokens[i:i + int(right_context_size) + 1] for i in inds]

        else:
            output_list = []

        return output_list

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
    if isinstance(tokens, list) and isinstance(word, str):

        if isinstance(left_n, int) and isinstance(right_n, int) and left_n >= 1 and right_n >= 1:
            concordances = get_concordance(tokens, word, left_n, right_n)
            adjacent_words = []
            for context in concordances:
                adjacent_words.append([context[0], context[-1]])

        elif (not isinstance(left_n, int) or left_n < 1) and (isinstance(right_n, int) and right_n >= 1):
            concordances = get_concordance(tokens, word, left_n, right_n)
            adjacent_words = []
            for context in concordances:
                adjacent_words.append([context[-1]])

        elif (not isinstance(right_n, int) or right_n < 1) and (isinstance(left_n, int) and left_n >= 1):
            concordances = get_concordance(tokens, word, left_n, -1)
            adjacent_words = []
            for context in concordances:
                adjacent_words.append([context[0]])

        else:
            return []

        return adjacent_words

    return []


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
        content_full = [' '.join(lst) for lst in content]
        content_output = '\n'.join(content_full)

        with open(path_to_file, 'w') as file:
            file.write(content_output)


def sort_list(concors, ind):
    sorted_list = []
    first_words = [concors[i][ind + 1] for i in range(len(concors)+1)]
    first_words.sort()
    for word in first_words:
        for context in concors:
            if context[ind + 1] == word:
                sorted_list.append(context)
                break

    return sorted_list


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
    if (isinstance(tokens, list) and isinstance(word, str) and isinstance(left_context_size, int) and
            isinstance(right_context_size, int) and isinstance(left_sort, bool)):

        concors = get_concordance(tokens, word, left_context_size, right_context_size)

        if left_sort and left_context_size > 0:
            output_list = sort_list(concors, -1)

        elif not left_sort and right_context_size > 0:
            output_list = sort_list(concors, left_context_size)

        else:
            output_list = []

        return output_list

    return []
