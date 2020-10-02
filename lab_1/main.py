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
    text = re.sub(r'[^a-z\s\n]', '', text)  # с помощью рег. выраж. убираю знаки препинания и числительные
    tokenize_list = text.split()
    return tokenize_list





def remove_stop_words(tokens: list, stop_words: list) -> list:
    """Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    stop_words = ['the', 'is']
    --> ['weather', 'sunny', 'man', 'happy']
    """
    new_tokens = []
    if isinstance(tokens, list) and isinstance(stop_words, list):#проверяем, списки ли это
        for token in tokens:
            if token not in stop_words: #проверяем входит ли слово в список стоп-слов
                new_tokens.append(token)
    return new_tokens





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
    dictionary = {} #создаем словарь
    if isinstance(tokens[0], str):
        for token in tokens:
            if token in dictionary:
                dictionary[token] += 1
            else:
                dictionary[token] = 1
    return dictionary



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
    sorted_list = []
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        sorted_list = sorted(freq_dict,key=freq_dict.get,reverse=True)
        sorted_list = sorted_list[:top_n]

    return sorted_list



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
    if isinstance(tokens, list) and isinstance(word, str) and not isinstance(left_context_size, bool) \
            and not isinstance(right_context_size, bool) and isinstance(right_context_size, int)\
            and isinstance(left_context_size,int):
        if right_context_size < 0:
            right_context_size = 0
        if left_context_size < 0:
            left_context_size = 0
        if right_context_size == 0 and left_context_size == 0:
            return []
        for index, element in enumerate(tokens):
            if element == word:

                new_concordance = tokens[index - left_context_size: index + right_context_size +1]
                concordance.append(new_concordance)
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
    if not isinstance(tokens, list) and not isinstance(word, str) and not isinstance(left_n, int)\
    and not isinstance(right_n, int)\
    and not left_n < 1 and not right_n < 1:
        return []
    previous_conc = get_concordance(tokens, word, left_n, right_n)
    ad_word = []
    for context in previous_conc:
        if left_n > 0 and right_n > 0:
            ad_word.append([context[0], context[-1]])
        elif right_n > 0:
            ad_word.append([context[-1]])
        elif left_n > 0:
            ad_word.append([context[0]])
    return ad_word



def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as concordance_file:
        data = concordance_file.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    with open(path_to_file, 'r', encoding='utf-8') as concordance_file:
        for concordance in content:
            return concordance_file.write('/n'. join(content))



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
