"""
Lab 1
A concordance extraction
"""


def tokenize(text: str):
    if not isinstance(text, str):
        return []
    tokens = []
    for token in text.lower().split():
        variable = ''
        for character in token:
            if character.isalpha():
                variable += character
        if len(variable) != 0:
            tokens.append(variable)
    return tokens


def remove_stop_words(tokens, stop_words):
    if isinstance(tokens, list) and isinstance(stop_words, list):
        new_list_token = [word for word in tokens if word not in stop_words]
        return new_list_token
    return []


def calculate_frequencies(tokens):
    if isinstance(tokens, list) and None not in tokens:
        dictionary = {}
        for i in tokens:
            dictionary[i] = tokens.count(i)
        return dictionary

    return {}


def get_top_n_words(dictionary, top_n):
    if isinstance(dictionary, dict) and isinstance(top_n, int):
        return [i[0] for i in sorted(list(dictionary.items()), key=lambda i: i[1], reverse=True)[:top_n]]
    return []


def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int):
    """
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    --> [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]

      

    """
    if not isinstance(tokens, list) or not isinstance(word, str) or None in tokens:
        return []
    if left_context_size is True or right_context_size is True or not isinstance(left_context_size, int) or not isinstance(right_context_size, int):
        return []
    if (left_context_size < 1) and (right_context_size < 1):
            return []
    ans = []
    for index, element in enumerate(tokens):
        if element == word:
            ans.append(tokens[index - left_context_size:index + right_context_size + 1])
    return ans


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
    with open(path_to_file, 'r', encoding='utf-8') as read_file:
        data = read_file.read()

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
