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
    if isinstance(text,str):
        text = text.lower()
        tokens = re.sub('[^a-zA-z \n]', '', text)
        tokens = tokens.split()
    else:
        tokens = []
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
    if not isinstance(tokens,list) or tokens == stop_words:
        return []
    if isinstance(stop_words,list) and (isinstance(tokens,list) or not tokens == stop_words):
        for i in tokens:
            if i in stop_words:
                tokens.remove(i)
    return tokens


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    freq_dict = {}
    if isinstance(tokens,list):
        for i in tokens:
            if isinstance(i,str):
                freq_dict[i] = tokens.count(i)
            else:
                freq_dict = {}
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
    top_words = []
    if isinstance(freq_dict,dict) and isinstance(top_n,int):
        if top_n >= len(freq_dict):
            top_n = len(freq_dict)
        list_freq_dict = list(freq_dict.items())
        list_freq_dict.sort(key=lambda i: i[1], reverse = True)
        for i in range(top_n):
            top_words.append(list_freq_dict[i][0])
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
    concordance = []
    if isinstance(left_context_size, bool) and isinstance(right_context_size, bool):
        return []
    if not isinstance(tokens, list) or not isinstance(word, str) \
            or not isinstance(left_context_size,int) or not isinstance(right_context_size,int):
        return []
    if (left_context_size > 0 or right_context_size > 0) and word in tokens and word != '':
        word_index = []
        for i, k in enumerate(tokens):
            if k == word:
                word_index.append(i)
        for i,k in enumerate(word_index):
            concordance.insert(i, [])
            if left_context_size > 0:
                concordance[i].extend(tokens[k - left_context_size:k])
            concordance[i].extend([word])
            if right_context_size > 0:
                concordance[i].extend(tokens[k+1:right_context_size+k+1])
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
    left_right_word = []
    concordance = get_concordance(tokens,word,left_n,right_n)
    for i,k in enumerate(concordance):
        left_right_word.insert(i,[])
        if left_n > 0:
            left_right_word[i].append(concordance[i][0])
        if right_n > 0:
            left_right_word[i].append(concordance[i][-1])

    return left_right_word


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
    with open(path_to_file, 'w') as file:
        for i in content:
            file.write(' '.join(i),'\n')


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

    sorted_concordance = []
    if isinstance(left_sort,bool) and isinstance(left_sort,int) and isinstance(right_context_size,int):
        sorted_concordance = get_concordance(tokens,word,left_context_size,right_context_size)
        if left_sort and left_context_size > 0:
            sorted_concordance.sort()
        elif not left_sort and right_context_size > 0:
            sorted_concordance.sort(key = lambda i: i[-left_context_size])
        else:
            sorted_concordance = []
    return sorted_concordance
