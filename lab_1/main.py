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
    if type (text) == str:
        clean_text = ''
        for sign in text:
            if sign.lower() in 'abcdefghijklmnopqrstuvwxyz ':
                clean_text += sign.lower()
        tokens = clean_text.split()
        return (tokens)
    else:
        return ([])
#tokenize (['big big hippo jumps over a baloon'])


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
    if type (tokens) == list:
        for token in tokens:
            for sign in token:
                if sign not in 'abcdefghijklmnopqrstuvwxyz':
                    tokens.clear()
                    break
        if type (stop_words) == list:
            for word in stop_words:
                for token in tokens:
                    if word == token:
                        tokens.remove(token)
            return(tokens)
        else:
            return (tokens)
    else:
        return ([])
#remove_stop_words ()

def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens{'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if type (tokens) == list:
        for token in tokens:
            for sign in token:
                if sign not in 'abcdefghijklmnopqrstuvwxyz':
                    tokens.clear()
                    break
        token_frequency = {token: tokens.count(token) for token in tokens}
        print (token_frequency)
        return(token_frequency)
    else:
        return ([])
#calculate_frequencies ('weather')

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
    if type (freq_dict) == dict and type (top_n) == int:
        for key in freq_dict.keys():
            for sign in key:
                if sign not in 'abcdefghijklmnopqrstuvwxyz':
                    return ([])
        for value in freq_dict.values():
            if type (value) != int:
                return ([])
        spisok_values = []
        spisok_index = []
        spisok_range_values = []
        spisok_keys = []
        spisok_range_keys = []
        for v in freq_dict.values():
            spisok_values.append(v)
        maximum = max(spisok_values)
        for v in range(0, maximum):
            for v in spisok_values:
                if v == maximum:
                    spisok_range_values.append(v)
                    spisok_index.append(spisok_values.index(v))
                    spisok_values[spisok_values.index(v)] = maximum + 1
            maximum -= 1
        for k in freq_dict:
            spisok_keys.append(k)
        for index in spisok_index:
            spisok_range_keys.append(spisok_keys[index])
        key_output = spisok_range_keys[0:top_n]
        return (key_output)
    else:
        return ([])
#get_top_n_words ()

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
    if type (tokens) == list and type (word) == str:
        for token in tokens:
            for sign in token:
                if sign not in 'abcdefghijklmnopqrstuvwxyz':
                    tokens.clear()
                    return ([])
        for sign in word:
            if sign not in 'abcdefghijklmnopqrstuvwxyz':
                return ([])
        if type (left_context_size) == int and type (right_context_size) == int:
            concordance = []
            for token in tokens:
                if token == word:
                    if left_context_size > 0:
                        left_context = tokens[tokens.index(token) - left_context_size: tokens.index(token)]
                    else:
                        left_context = []
                    if right_context_size > 0:
                        right_context = tokens[tokens.index(token) + 1: tokens.index(token) + right_context_size + 1]
                    else:
                        right_context = []
                    if left_context_size < 1 and right_context_size < 1:
                        return ([])
                    current_context_list = left_context
                    current_context_list.append(token)
                    current_context_list.extend (right_context)
                    concordance.append(current_context_list)
                    tokens.insert(tokens.index(token), 'буферный элемент')
                    tokens.remove(token)
            return (concordance)
        else:
            return ([])
    else:
        return ([])
#get_concordance (['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy', 'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad'], 'the', 1, 1)



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
    concordance = get_concordance (tokens, word, left_n, right_n)
    if type(left_n) == int and type(right_n) == int:
        for spisok in concordance:
            for token in spisok:
                if token == word:
                    if left_n > 0:
                        left_word = spisok[spisok.index(token) - left_n]
                    else:
                        left_word = ''
                    if right_n > 0:
                        right_word = spisok[spisok.index(token) + right_n]
                    else:
                        right_word = ''
                    if left_n < 1 and left_n < 1:
                        return ([])
                    current_words = [left_word, right_word]
                    adjacent_words.append(current_words)
    else:
        return ([])
#get_adjacent_words(['yesterday', 'the', 'weather', 'was', 'sunny', 'and', 'windy', 'today', 'it', 'is', 'sunny', 'and', 'windy', 'too'], 'sunny', 3, 1)




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
    file = open (path_to_file, 'w')
    for spisok in content:
        text = str(spisok) + '\n'
        file.write (text)
#write_to_file(r'C:\Users\user\2020-2-level-labs\lab_1\report.txt', [['the', 'weather'], ['sunny', 'the', 'man'], ['happy', 'the', 'dog'], ['but', 'the', 'cat']])



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
