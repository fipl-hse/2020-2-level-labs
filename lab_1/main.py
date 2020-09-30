"""
Lab 1
A concordance extraction
"""
import re


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as fs:
        data = fs.read()

    return data


text = read_from_file('data.txt')


def tokenize(text:str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    pass
    if not isinstance(text, str):  # check type (принадлежность)
        tokens = []
        return tokens
    reg = re.compile('[^a-zA-Z \n`]')
    clean_text = reg.sub('', text)
    clean_text = clean_text.lower()
    tokens = clean_text.split()
    return tokens


stop_words = read_from_file('stop_words.txt')
stop_words = stop_words.split()

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
    pass
    if not isinstance(tokens, list) or not tokens or not isinstance(stop_words, list):  #check for emptiness
        return []
    if (isinstance(tokens, list) and tokens) and not (isinstance(stop_words, list) and stop_words):
        return tokens

    copy_text = tokens[:]   #copy list
    for words in tokens:
        if words in stop_words:
            copy_text.remove(words)

    return copy_text




def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """

    pass
    if isinstance(tokens, list) and tokens: #check
        for words in tokens:
            if not isinstance(words, str):  #if not word
                return {}
        freq_dict = {words:tokens.count(words)}
        return freq_dict
    return{}


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
    pass
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int) or not freq_dict or not top_n >= 1:
        return []

    top_list = list(freq_dict.items())
    top_list.sort(key=lambda i:i[1])    #sort by keys(2 element) for less volume-lambda

    n_top_list = []
    for f_word in top_list[:top_n]:
        n_top_list.append(f_word[0])
    return n_top_list



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
    pass
    if isinstance(right_context_size, bool) or isinstance(left_context_size, bool):     #check for emptiness
        return []

    if not isinstance(tokens, list) and not isinstance(word, str) \
            and not isinstance(right_context_size, int) and not isinstance(left_context_size, int):       #check type
        return []

    part_text = []
    for ind,elem in enumerate(tokens):  #make list with numbers & tokens
        if elem == word:
            if left_context_size > 0 and right_context_size > 0:
                for i in ind:
                    part_text.append(tokens[i - left_context_size:i+ right_context_size + 1])
            elif left_context_size <= 0:
                for i in ind:
                    part_text.append(tokens[i:i + int(right_context_size) + 1])
            elif right_context_size <= 0:
                for i in ind:
                    part_text.append(tokens[i - left_context_size:i + 1])
            else:
                part_text = []
    return part_text




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
