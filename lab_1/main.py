"""
Lab 1
A concordance extraction
"""
import re


def tokenize(text: str) -> list:
    tokens = []
    if type(text) == str:
        tokens = text.lower()
        tokens = re.sub(r'[^a-z\s\n]', '', tokens).split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list:
    clean_tokens = []

    if isinstance(tokens, list) and isinstance(stop_words, list):
        for i in tokens:
            if i not in stop_words:
                clean_tokens.append(i)
    else:
        clean_tokens = []
    return clean_tokens


def calculate_frequencies(tokens: list) -> dict:
    freq_dict = {}
    if isinstance(tokens, list)  and len(tokens) > 0:
        if type(tokens[0]) == str:
            for i in tokens:
                if i in freq_dict:
                    freq_dict[i] += 1
                else:
                    freq_dict[i] = 1
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    sorted_dict = []
    if isinstance(freq_dict, dict) and top_n > 0:
        sorted_dict = sorted(freq_dict, key=freq_dict.get, reverse=True)
        sorted_dict = sorted_dict[:top_n]
    return sorted_dict


def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int) -> list:
    check_left = isinstance(left_context_size, int) and left_context_size > 0 and not isinstance(left_context_size, bool)
    check_right = isinstance(right_context_size, int) and right_context_size > 0 and not isinstance(right_context_size, bool)
    check_tokens = isinstance(tokens, list)
    word_check = isinstance(word, str)
    all_context = []

    if check_tokens and word_check:
        check = word in tokens
    else:
        return all_context

    for ind, token  in enumerate(tokens):
        if token == word:
            if check_left and check_right and check:
                all_context.append(tokens[ind-left_context_size:ind+right_context_size+1])
            elif check_left and check:
                all_context.append(tokens[ind-left_context_size:ind+1])
            elif check_right and check:
                all_context.append(tokens[ind:ind+right_context_size+1])

    return all_context


def get_adjacent_words(tokens: list, word: str, left_n: int, right_n: int) -> list:
    concordance = get_concordance(tokens, word, left_n, right_n)
    concordance_n = []
    if isinstance(tokens, list) and isinstance(word, str):
        for theword in concordance:
            if left_n == 0:
                concordance_n.append([theword[-1]])
            elif right_n == 0:
                concordance_n.append([theword[0]])
            else:
                concordance_n.append([theword[0], theword[-1]])
    return concordance_n


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
