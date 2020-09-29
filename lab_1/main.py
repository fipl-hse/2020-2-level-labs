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
    if isinstance(text, str):
        token_list = []
        for i in text.split():
            if not i.isalpha():
                for s in i:
                    if not s.isalpha():
                        i = i.replace(s, '')
            if i.isalpha():
                token_list.append(i.lower())
        return token_list
    else:
        return []


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
    elif not isinstance(stop_words, list) or not stop_words:
        return tokens
    else:
        tokens1 = [i for i in tokens if i not in stop_words]
        return tokens1


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if not isinstance(tokens, list) or not all(isinstance(i, str) for i in tokens):
        return {}
    else:
        freq_dict = {}
        for i in tokens:
            if i not in freq_dict:
                freq_dict[i] = tokens.count(i)
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
    word_list = []
    freq_list = []
    top_n_words_list = []
    if isinstance(freq_dict, dict) and isinstance(top_n, int) and top_n >= 0:
        for k, v in freq_dict.items():
            word_list.append(k)
            freq_list.append(v)
        if top_n > len(word_list):
            top_n = len(word_list)
        for i in range(top_n):
            max_num_index = freq_list.index(max(freq_list))
            freq_list[max_num_index] = 0
            top_n_words_list.append(word_list[max_num_index])
        return top_n_words_list
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
    if (not isinstance(tokens, list) or not isinstance(word, str) or not word.isalpha() or
            type(left_context_size) is not int or type(right_context_size) is not int or
            (left_context_size < 1 and right_context_size < 1)):
        return []
    else:
        concordance = []
        if left_context_size < 0:
            left_context_size = 0
        elif right_context_size < 0:
            right_context_size = 0
        for i in tokens:
            if i == word:
                w_ind = tokens.index(i)
                concordance.append(tokens[w_ind - left_context_size: w_ind + right_context_size + 1])
                tokens.remove(i)
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
    adjacent_words_list = []
    for i in concordance:
        if left_n <= 0:
            adjacent_words_list.append([i[-1]])
        elif right_n <= 0:
            adjacent_words_list.append([i[0]])
        else:
            adjacent_words_list.append([i[0], i[-1]])
    return adjacent_words_list


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
    for i in content:
        content[content.index(i)] = ' '.join(i)
    with open(path_to_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(content))


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
    concordance = get_concordance(tokens, word, left_context_size, right_context_size)
    sorted_concordance = []
    if type(left_sort) is not bool:
        return []
    elif left_sort:
        left_words_list = [i[0] for i in concordance]
        for i in sorted(left_words_list):
            for l in concordance:
                if i == l[0]:
                    sorted_concordance.append(l)
                    concordance.remove(l)
                    break
        return sorted_concordance
    else:
        right_words_list = [i[-1] for i in concordance]
        for i in sorted(right_words_list):
            for l in concordance:
                if i == l[-1]:
                    sorted_concordance.append(l)
                    concordance.remove(l)
                    break
        return sorted_concordance
