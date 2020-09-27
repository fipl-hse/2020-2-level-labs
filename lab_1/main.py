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
    if type(text) != str:
        return []
    lines = text.split('\n')
    tokens = []
    for words in lines:
        words = words.split()
        for word in words:
            word = word.lower()
            word_new = ''
            for letter in word:
                if letter.isalpha():
                    word_new += letter
            if word_new != '':
                tokens.append(word_new)
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
    if type(tokens) != list:
        return []
    elif type(stop_words) != list:
        return tokens
    for stop_word in stop_words:
        while stop_word in tokens:
            tokens.remove(stop_word)
    return tokens         


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if type(tokens) != list or None in tokens:
        return {}
    freq_dict = {token: tokens.count(token) for token in tokens}
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
    if type(freq_dict) != dict or type(top_n) != int:
        return []
    top_words = []
    sorted_dict = {k: freq_dict[k] for k in sorted(freq_dict, key=freq_dict.get, reverse=True)}
    for key in sorted_dict:
        top_words.append(key)
    return top_words[:top_n]


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
    if type(tokens) != list or type(word) != str:
        return []
    elif type(left_context_size) != int or type(right_context_size) != int:
        return []
    elif left_context_size < 1 and right_context_size < 1:
        return []
    for number, token in enumerate(tokens):
        context = []
        if token == word:
            if right_context_size < 1 and left_context_size >= 1:
                left_size = left_context_size
                while left_size != 0:
                    if number - left_size >= 0:
                        context.append(tokens[number-left_size])
                    left_size -= 1
                context.append(token)
            elif right_context_size >= 1 and left_context_size < 1:
                context = [token]
                iterations = 1
                right_size = right_context_size
                while right_size != 0:
                    if len(tokens) > number + iterations:
                        context.append(tokens[number+iterations])
                    right_size -= 1
                    iterations += 1
            elif right_context_size >= 1 and left_context_size >= 1:
                iterations = 1
                left_size = left_context_size
                right_size = right_context_size
                while left_size != 0:
                    if number - left_size >= 0:
                        context.append(tokens[number-left_size])
                    left_size -= 1
                context.append(token)
                while right_size != 0:
                    if len(tokens) > number + iterations:
                        context.append(tokens[number+iterations])
                    right_size -= 1
                    iterations += 1
        if context != []:
            concordance.append(context)
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
    if type(tokens) != list or type(word) != str:
        return []
    elif type(left_n) != int or type(right_n) != int:
        return []
    elif left_n < 1 and right_n < 1:
        return []
    concordance = get_concordance (tokens, word, left_n, right_n)
    for usage in concordance:
        pair_of_words = []
        for number, token in enumerate(usage):
            if token == word:
                if left_n >= 1 and right_n < 1:
                    if left_n > len(usage[:number]):
                        adjacent_words.append([usage [0]])
                    else:
                        adjacent_words.append([usage [number - left_n]])
                elif left_n < 1 and right_n >= 1:
                    if right_n > len(usage[number+1:]):
                        adjacent_words.append([usage [-1]])
                    else:
                        adjacent_words.append([usage [number + right_n]])
                elif left_n >= 1 and right_n >= 1:
                    if left_n > len(usage[:number]):
                        pair_of_words.append(usage [0])
                    else:
                        pair_of_words.append(usage [number - left_n])
                    if right_n > len(usage[number+1:]):
                        pair_of_words.append(usage [-1])
                    else:
                        pair_of_words.append(usage [number + right_n])
        if pair_of_words != []:
            adjacent_words.append(pair_of_words)
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
    if type(path_to_file) == str and type(concordance) == list:
        with open(path_to_file, 'w', encoding='utf-8') as file:
            for line in concordance:
                file.write(' '.join(line)+'\n')
            

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
    if type(left_sort) != bool:
        return []
    sorted_concordance = []
    concordance = get_concordance (tokens, word, left_context_size, right_context_size)

    def sort_by_first_item(concordance):
        if token == usage[0] and usage.count(token) == 1:
            return []
        return concordance[0]

    def sort_by_item_after_word(concordance):
        if token == usage[-1] and usage.count(token) == 1:
            return []
        elif len(concordance) <= number+1:
            return concordance[-1]
        return concordance[number+1]

    for usage in concordance:
        for number, token in enumerate(usage):
            if token == word:
                if left_sort == True:
                    if sort_by_first_item (concordance) == []:
                        return []
                    sorted_concordance = sorted(concordance, key=sort_by_first_item)
                elif left_sort == False:
                    if sort_by_item_after_word (concordance) == []:
                        return []
                    sorted_concordance = sorted(concordance, key=sort_by_item_after_word)
    return sorted_concordance

