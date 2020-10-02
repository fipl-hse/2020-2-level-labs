"""
Sample change by me
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
    if isinstance (text, str):
        clean_text_list = []
        raw_text_list = text.split()
        for word in raw_text_list:
            new_word = ''
            for sign in word:
                if sign.lower() in 'abcdefghijklmnopqrstuvwxyz ':
                    new_word += sign.lower()
            clean_text_list.append(new_word)
        for element in clean_text_list:
            if len(element) == 0:
                clean_text_list.pop(clean_text_list.index(element))
        return clean_text_list
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
    new_tokens = []
    if isinstance(tokens, list) and isinstance (stop_words, list):
        for token in tokens:
            if token not in stop_words:
                new_tokens.append(token)
        return new_tokens
    return []


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if isinstance(tokens, list):
        for token in tokens:
            if not isinstance (token, str):
                return {}
        token_frequency = {token: tokens.count(token) for token in tokens}
        return token_frequency
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
    if isinstance (freq_dict, dict) and isinstance (top_n, int):
        if len(freq_dict) != 0:
            for value in freq_dict.values():
                if not isinstance (value, int):
                    return []
            list_of_values = []
            list_of_index = []
            list_of_ranged_values = []
            list_of_keys = []
            list_of_ranged_keys = []
            for value_1 in freq_dict.values():
                list_of_values.append(value_1)
            maximum = max(list_of_values)
            for value_1 in range(0, maximum):
                for value in list_of_values:
                    if value == maximum:
                        list_of_ranged_values.append(value)
                        list_of_index.append(list_of_values.index(value))
                        list_of_values[list_of_values.index(value)] = maximum + 1
                maximum -= 1
            for k in freq_dict:
                list_of_keys.append(k)
            for index in list_of_index:
                list_of_ranged_keys.append(list_of_keys[index])
            key_output = list_of_ranged_keys[0:top_n]
            return key_output
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
    if not isinstance(left_context_size, int) or not isinstance(right_context_size, int) \
            or not isinstance(tokens, list) or not isinstance(word, str):
        return []
    if isinstance(left_context_size, bool) or isinstance(right_context_size, bool):
        return []
    concordance = []
    for token in tokens:
        if token == word and isinstance (token, str):
            if left_context_size > 0:
                left_context = tokens[tokens.index(token) - left_context_size: tokens.index(token)]
            else:
                left_context = []
            if right_context_size > 0:
                right_context = tokens[tokens.index(token) + 1: tokens.index(token) + right_context_size + 1]
            else:
                right_context = []
            if left_context_size < 1 and right_context_size < 1:
                return []
            current_context_list = left_context
            current_context_list.append(token)
            current_context_list.extend (right_context)
            concordance.append(current_context_list)
            tokens.insert(tokens.index(token), 'буферный элемент')
            tokens.remove(token)
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
    if not isinstance(left_n, int) or not isinstance(right_n, int) \
            or not isinstance(tokens, list) or not isinstance(word, str):
        return []
    if isinstance(left_n, bool) or isinstance(right_n, bool):
        return []
    adjacent_words = []
    concordance = get_concordance(tokens, word, left_n, right_n)
    for small_list in concordance:
        current_words = []
        if left_n > 0 and right_n > 0:
            current_words.append(small_list[0])
            current_words.append(small_list[-1])
        elif left_n < 1 and right_n > 0:
            current_words.append(small_list[-1])
        elif right_n < 1 and left_n > 0:
            current_words.append(small_list[0])
        elif left_n < 1 and right_n < 1:
            return []
        adjacent_words.append(current_words)
    return adjacent_words


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as path:
        data = path.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    text = ''
    file = open (path_to_file, 'w')
    for small_list in content:
        for word in small_list:
            text += word + ' '
        text += '\n'
    file.write (text)


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
    if not isinstance(left_context_size, int) or not isinstance(right_context_size, int) \
            or not isinstance(tokens, list) or not isinstance(word, str):
        return []
    if isinstance(left_context_size, bool) or isinstance(right_context_size, bool) or not isinstance(left_sort, bool):
        return []
    concordance = get_concordance(tokens, word, left_context_size, right_context_size)
    if left_sort is True and left_context_size > 0:
        return sorted (concordance)
    if left_sort is False and right_context_size > 0:
        return sorted(concordance, key = lambda list_of_words: list_of_words[list_of_words.index (word) + 1])
    return []
