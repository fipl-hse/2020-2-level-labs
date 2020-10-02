import re
import string
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
    if not isinstance(text, str) or not text:
        return []

    prepared_text = re.sub('[^a-zA-Z \n`]', '', text).lower()
    return prepared_text.split()


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

    result = []
    for word in tokens:
        if word not in stop_words:
            result.append(word)
            
    return result


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """

    if not(isinstance(tokens, list)) or len(tokens) == 0:
        return {}
    
    if not(isinstance(tokens[0], str)):
        return {}
           
    result = {}
    tokens_set = set(tokens)
    for word in tokens_set:
        result[word] = tokens.count(word)

    return result


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

    if len(freq_dict) == 0 or top_n == 0:
        return []
    
    freq_array = []
    for key, val in freq_dict.items():
        freq_array.append([val, key])
    freq_array.sort(reverse = True, key=lambda x: x[0])

    result = []
    for i in range(top_n):
        try:
            result.append(freq_array[i][1])
        except IndexError:
            break


    return result


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
    r_is_int = isinstance(right_context_size, int)
    l_is_int = isinstance(left_context_size, int)
    
    l_is_bool = isinstance(left_context_size, bool)
    r_is_bool = isinstance(right_context_size, bool)

    if not(r_is_int) and not(l_is_int):
        return []

    if not(isinstance(tokens, list)) or not(isinstance(word, str)):
        return []

    if l_is_bool and r_is_bool:
        return []
    '''
    if len(tokens) == 0 or not(isinstance(tokens[0], str)):
        return []
    '''
    if left_context_size <= 0 and right_context_size <= 0:
        return []
    
    if word not in tokens:
        return []
    
    if right_context_size < 0:
        right_context_size = 0
    if left_context_size < 0:
        left_context_size = 0

    result = []
    A = []
    for ind, val in enumerate(tokens):
        if val == word:
            A.append(ind)
    for ind in A:
        result.append(tokens[ind - left_context_size:ind + right_context_size + 1])
    return result


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
    if not isinstance(tokens, list) or not isinstance(word, str):
        return []

    left_check = isinstance(left_n, int)
    right_check = isinstance(right_n, int)
    if (not left_check) and (not right_check):
        return []

    result = []
    for i in range(len(tokens)):
        if tokens[i] == word:
            A = []
            if left_n == 0:
                concordance_n.append([tokens[i + right_n]])
            elif right_n == 0:
                concordance_n.append([tokens[i - left_n]])
            else:
                concordance_n.append([tokens[i + right_n], tokens[i - left_n]])
            result.append(A)

    return result


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
    with open(path_to_file, 'w', encoding='utf-8') as f:
        print(content, file = f)
        

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

