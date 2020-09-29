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
    if type(text) == str:
        splitted = text.split()
        tokens = []
        for word in splitted:
            token = []
            for symbol in word:
                if symbol.isalpha():
                    token.append(symbol)
                elif symbol.isdigit():
                    return []
            if len(token):
                tokens.append("".join(token))
        tokens = [token.lower() for token in tokens]
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
    if type(tokens) != list:
        scraped = []
    else:
        if type(stop_words) != list:
            return tokens
        else:
            scraped = [token for token in tokens if token not in stop_words]
    return scraped


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    frequencies = {}
    if type(tokens) != list:
        pass
    else:
        for token in tokens:
            if type(token) == str:
                if token not in frequencies:
                    frequencies[token] = 1
                else:
                    frequencies[token] += 1
    return frequencies


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
        top = []
    else:
        top = [i[0] for i in sorted(list(freq_dict.items()), key=lambda i: i[1], reverse=True)[:top_n]] # Marina from future, will you kindly shorten this line
    return top


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
    lcs_checked = False
    rcs_checked = False
    if type(tokens) != list or type(word) != str:
        pass
    else:
        if type(left_context_size) == int:
            if left_context_size >= 1:
                lcs_checked = True
        if type(right_context_size) == int:
            if right_context_size >= 1:
                rcs_checked = True
        if not rcs_checked and not lcs_checked:
            pass
        else:
            for index, item in enumerate(tokens):
                if item == word:
                    subconcor = []
                    if lcs_checked:
                        shift = 1
                        for _ in range(left_context_size):
                            try:
                                subconcor.append(tokens[index - shift])
                                shift += 1
                            except IndexError:
                                break
                    subconcor.append(word)
                    if rcs_checked:
                        shift = 1
                        for _ in range(right_context_size):
                            try:
                                subconcor.append(tokens[index + shift])
                                shift += 1
                            except IndexError:
                                break
                    concordance.append(subconcor)
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
    adj_words = []
    if type(tokens) != list or type(word) != str:
        pass
    else:
        if type(left_n) != int:
            left_n = 0
        if type(right_n) != int:
            right_n = 0
        concordance = get_concordance(tokens, word, left_n, right_n)
        for context in concordance:
            subcontext = []
            for end in [context[0], context[-1]]:
                if end != word:
                    subcontext.append(end)
            adj_words.append(subcontext)
    return adj_words


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
    with open('report.txt', 'w', encoding='utf8') as file:
        for example in content:
            file.writelines([i + '\n' for i in example])


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
