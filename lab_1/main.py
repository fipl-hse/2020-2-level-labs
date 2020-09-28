"""
Lab 1
A concordance extraction
"""

def tokenize(text):
    if type(text) == str:
        text = text.lower()
        for symbol in text:
            if symbol.isalpha() == False and symbol != ' ' and symbol != '\n':
                text = text.replace(symbol, '')
            elif symbol == '\n':
                text = text.replace(symbol, ' ')
        tokens_list = text.split()
        return (tokens_list)
    else: return []


def remove_stop_words(tokens_list,stop_words):
    if type(tokens_list) == list and type(stop_words) == list:
        for word in stop_words:
            while word in tokens_list:
                tokens_list.remove(word)
        return tokens_list
    else: return []


def calculate_frequencies(tokens_list):
    if type(tokens_list) == list and None not in tokens_list:
        frequency_dictionary = {}
        for token in tokens_list:
            if token in frequency_dictionary:
                frequency_dictionary[token] += 1
            else: frequency_dictionary[token] = 1
        return(frequency_dictionary)
    else: return {}


def get_top_n_words(frequency_dictionary, top_n):
    top_tokens = []
    top_n_tokens = []
    check_value = 0
    if type(frequency_dictionary) == dict and type(top_n) == int:
        for key, value in frequency_dictionary.items():
            if value > check_value:
                check_value = value
                top_tokens.insert(0, key)
            elif value == check_value:
                top_tokens.insert(1, key)
            else: top_tokens.append(key)
        if top_n > len(top_tokens):
            return (top_tokens)
        else:
            for index in range(top_n):
                top_n_tokens.append(top_tokens[index])
            return (top_n_tokens)
    else: return []


def get_concordance(tokens_list,word,left_context_size,right_context_size):
    concordance = []
    correct_circumstance = (word != '') and (type(word) == str) and (tokens_list != []) and (type(tokens_list) == list) and (None not in tokens_list)\
                               and (type(left_context_size) == int) and (type(right_context_size) == int) and (left_context_size >= 1 or right_context_size >= 1)
    if correct_circumstance:
        for index,token in enumerate(tokens_list):
            if token == word:
                concordance.extend([tokens_list[index - left_context_size:index + right_context_size + 1:1]])
        return (concordance)
    else: return []


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
    pass


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
    pass
