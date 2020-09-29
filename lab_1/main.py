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
    if not isinstance(text, str):
        return []
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s ]', '', text)
    text = text.split()
    return text

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
    new_text = [word for word in tokens if word not in stop_words]
    return new_text



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
    for word in tokens:
        if isinstance(word, str):
            freq_dic = {word: tokens.count(word) for word in tokens}
            return freq_dic
        else:
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
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        list_of_items = list(freq_dict.items())
        list_of_items.sort(key=lambda x: x[1], reverse=True)
        top_n_words = []
        for pair_el in list_of_items:
            top_n_words.append(pair_el[0])
        return top_n_words[:top_n]
    else:
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

    l_context_b = isinstance(left_context_size, bool)
    r_context_b = isinstance(right_context_size, bool)
    l_context_int = isinstance(left_context_size, int)
    r_context_int = isinstance(right_context_size, int)
    check_circ = (not isinstance(tokens,list) or not isinstance(word,str) \
                  or word not in tokens \
                  or (l_context_b and r_context_b) \
                  or (not l_context_int and not r_context_int) \
                  or (left_context_size < 1 and right_context_size < 1))
    if check_circ:
        return []
    concordance = []
    index_list = []
    for index, token in enumerate(tokens):
        if token == word:
            index_list.append(index)
    for ind in index_list:
        concordance.append(tokens[ind - left_context_size:ind + right_context_size + 1])
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

    concordance = get_concordance(tokens, word, left_n, right_n)
    conc_pair = []
    new_check = (isinstance(tokens,list) and isinstance(word,str) \
                 and not isinstance(left_n, bool) and not isinstance(right_n, bool))
    if new_check:
        for w in concordance:
            if left_n == 0:
                conc_pair.append([w[-1]])
            elif right_n == 0:
                conc_pair.append([w[0]])
            else:
                conc_pair.append([w[0], w[-1]])
    return conc_pair




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
