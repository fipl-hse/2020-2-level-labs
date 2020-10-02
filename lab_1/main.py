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
    if not isinstance(text, str):
        return []
    if isinstance(text, str):
        tokens = ''
        text = text.lower()
        text = text.replace('\n', ' ')
        for i in text:
            if i.isalpha() or i == ' ':
                tokens += i
        tokens = tokens.split(' ')
        while '' in tokens:
            tokens.remove('')

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
    without_stop_words = []
    if not isinstance(tokens, list) or len(tokens) == 0:
        return []
    if not isinstance(stop_words, list) or len(stop_words) == 0:
        return tokens
    if isinstance(tokens, list) and len(tokens) != 0 and len(stop_words) != 0 and isinstance(stop_words, list):
        for element in tokens:
            if element not in stop_words:
                without_stop_words.append(element)

    return without_stop_words



def calculate_frequencies(without_stop_words: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    freq = {}
    if not isinstance(without_stop_words, list) or len(without_stop_words) < 1 \
            or None in without_stop_words:
        return {}
    if isinstance(without_stop_words, list) and len(without_stop_words) >= 1:
        for i in without_stop_words:
            num = without_stop_words.count(i)
            element = {i: num}
            freq.update(element)

    return freq




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
    top_n_words = []
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int) or None in freq_dict:
        return []
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        freq_k = list(freq_dict.keys())
        freq_v = list(freq_dict.values())
        freq_s = freq_v.copy()
        freq_v.sort(reverse=True)
        for i in freq_v[:top_n]:
            num = freq_s.index(i)
            top_n_words.append(freq_k[num])
            freq_k.remove(freq_k[num])

    return top_n_words




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
    right_context_size = 3;
    --> [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]
    """
    concordance1 = []
    test1 = isinstance(tokens, list)
    test2 = isinstance(word, str)
    test3 = isinstance(left_context_size, int)
    test4 = isinstance(right_context_size, int)
    if not test1 or not test2 or not test3 or not test4 or word not in tokens:
        return []

    if isinstance(right_context_size, bool) or isinstance(left_context_size, bool):
        return []

    if left_context_size > 0 and right_context_size > 0:
        words = tokens.count(word)
        num = tokens.index(word)
        concordance = tokens[num - left_context_size:num] + tokens[num:num + right_context_size + 1]
        concordance1.append(concordance)
        tokens.remove(word)
        if words > 1:
            while words != 1:
                new_num = tokens.index(word)
                new_concordance = tokens[new_num - left_context_size:new_num] + \
                                    tokens[new_num:new_num + right_context_size + 1]
                concordance1.append(new_concordance)
                words -= 1
                tokens.remove(word)
    elif right_context_size > 0:
        num = tokens.index(word)
        concordance = tokens[num:num + right_context_size + 1]
        concordance1.append(concordance)
    elif left_context_size > 0:
        num = tokens.index(word)
        concordance = tokens[num - left_context_size:num + 1]
        concordance1.append(concordance)

    return concordance1




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
    all_adjacent_words = []
    context = []
    test1 = isinstance(tokens, list)
    test2 = isinstance(word, str)
    test3 = isinstance(left_n, int)
    test4 = isinstance(right_n, int)
    if not (test1 and test2 and word in tokens and test3 and test4):
        return []
    if isinstance(left_n, bool) or isinstance(right_n, bool):
        return []
    if right_n > 0 and left_n > 0:
        concordance = get_concordance(tokens, word, left_n, right_n)
        print(concordance)
        for text in concordance:
            all_adjacent_words.append([text[0], text[-1]])
    elif right_n > 0:
        concordance = get_concordance(tokens, word, left_n, right_n)
        for text in concordance:
            all_adjacent_words.append([text[-1]])
    elif left_n > 0:
        concordance = get_concordance(tokens, word, left_n, right_n)
        for text in concordance:
            all_adjacent_words.append([text[0]])
    return all_adjacent_words





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
    all_context = ''
    with open(path_to_file, 'w') as report:
        for text in content:
            context = ' '.join(text) + '\n'
            all_context += context

        report.write(all_context)

    return report


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
