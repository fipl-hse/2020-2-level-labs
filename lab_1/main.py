"""
Lab 1
A concordance extraction
"""
def tokenize(f):
    if not isinstance(f, str):
        return []
    tokens = []
    for token in f.lower().split():
        variable = ''
        for character in token:
            if character.isalpha():
                variable += character

        if len(variable) != 0:
            tokens.append(variable)
    return tokens

        

def remove_stop_words(tokens, stop_words):
    if isinstance(tokens, list) or isinstance(stop_words, list):
        new_list_token = [word for word in tokens if word not in stop_words]
        return list(new_list_token)
    return []


def calculate_frequencies(tokens):
    if not isinstance(tokens, list) or None in tokens:
        return {}
    global tokenize_text
    dictionary = {}
    for i in tokens:
        dictionary[i] = tokenize_text.count(i)
    return dictionary


def get_top_n_words(dictionary, n):
    if not isinstance(dictionary, dict) or not isinstance(n, int) or None in dictionary:
        return []
    ans = []
    cnt = 0
    for w in sorted(dictionary, key=dictionary.get, reverse=True):
        ans.append(w)
        cnt += 1
        if cnt == n:
            return ans

def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int):
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
    if not isinstance(tokens, list) or not isinstance(word, str) \
            or None in tokens:
        return []
    iter = [i for i in range(len(tokens)) if tokens[i] == word]
    ans = []
    for i in iter:
        if (i - left_context_size) >= 0 and (i + right_context_size < len(tokens)):
            ans.append(tokens[i - left_context_size: i + right_context_size + 1])
        elif (i - left_context_size) >= 0:
            ans.append(tokens[i - left_context_size:])
        else:
            ans.append(tokens[:i + right_context_size + 1])
                                       
    return any
                               

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
