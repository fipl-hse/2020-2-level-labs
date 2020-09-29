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
    if not type(text) == str: return []
    text = text.lower()
    for symbol in text:
        if symbol.isalpha() is False and symbol != ' ' and symbol != '\n':
            text = text.replace(symbol, '')
        elif symbol == '\n':
            text = text.replace(symbol, ' ')
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
    if not type(tokens) == list or not type(stop_words) == list: return []
    for word in stop_words:
        while word in tokens:
            tokens.remove(word)
    return tokens


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if not type(tokens) == list or None in tokens: return {}
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    return freq_dict


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
    top_tokens = []
    top_n_tokens = []
    check_value = 0
    if not type(freq_dict) == dict or not type(top_n) == int: return []
    for key, value in freq_dict.items():
        if value > check_value:
            check_value = value
            top_tokens.insert(0, key)
        elif value == check_value:
            top_tokens.insert(1, key)
        else:
            top_tokens.append(key)
    if top_n > len(top_tokens):
        return top_tokens
    else:
        for index in range(top_n):
            top_n_tokens.append(top_tokens[index])
        return top_n_tokens


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
    wrong_circumstance = word == '' or not type(word) == str or tokens == [] \
     or not type(tokens) == list or None in tokens \
     or not type(left_context_size) == int or not type(right_context_size) == int \
     or (left_context_size < 1 and right_context_size < 1)
    if wrong_circumstance: return []
    for index, token in enumerate(tokens):
        if token == word:
            concordance.extend([tokens[index - left_context_size:index + right_context_size + 1:1]])
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
    adjacent_words = []
    wrong_circumstance = word == '' or not type(word) == str or tokens == [] \
     or not type(tokens) == list or None in tokens \
     or not type(left_n) == int or not type(right_n) == int \
     or (left_n < 1 and right_n < 1)
    if wrong_circumstance: return []
    concordance = get_concordance(tokens, word, left_n, right_n)
    for part_concordance in concordance:
        for index in range(len(part_concordance)):
            if part_concordance[index] == word:
                if left_n == 0 and right_n > (len(part_concordance) - index):
                    adjacent_words.extend([[part_concordance[-1]]])
                elif right_n == 0 and left_n > index:
                    adjacent_words.extend([[part_concordance[0]]])
                elif left_n == 0:
                    adjacent_words.extend([[part_concordance[index + right_n]]])
                elif right_n == 0:
                    adjacent_words.extend([[part_concordance[index - left_n]]])
                elif left_n > index:
                    adjacent_words.extend([[part_concordance[0], part_concordance[index + right_n]]])
                elif right_n > (len(part_concordance) - index):
                    adjacent_words.extend([[part_concordance[index - left_n], part_concordance[-1]]])
                else:
                    adjacent_words.extend([[part_concordance[index - left_n], part_concordance[index + right_n]]])
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
    concordance_text = []
    for concordance in content:
        concordance_str = ' '.join(concordance)
        concordance_text.append(concordance_str)
    concordance_text = '\n'.join(concordance_text)
    fail_concordance = open(path_to_file, 'w')
    fail_concordance.write(concordance_text)
    fail_concordance.close()


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
