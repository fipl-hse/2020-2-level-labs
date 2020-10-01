"""
Lab 1
A concordance extraction
"""


def tokenize(text):
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    if isinstance(text,str):
        text = text.lower()
        litter = '!@#$%^&*()_+=-\;№:?[]{},.<>~\'\"/|\\1234567890'
        tokens = ''
        for c in text:
            if c not in litter:
                tokens += c
        tokens = tokens.split()
        return tokens
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
    if isinstance(tokens,list) and isinstance(stop_words,list):
        tokens_without_stop=[]
        for i in tokens:
            if i not in stop_words:
                tokens_without_stop.append(i)
        return tokens_without_stop
    return []


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if isinstance(tokens,list) and all (tokens):
        frequences = []
        for i in tokens:
            frequences.append (tokens.count(i) )
        freq_dict = {tokens[i]: frequences[i] for i in range(len(frequences))}
        return freq_dict
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
    if isinstance(freq_dict,dict)and isinstance(top_n,int):
        list_dict = list(freq_dict.items())
        list_dict.sort( key=lambda i: i[1], reverse=True)
        top_words=[]
        for i in list_dict:
            top_words.append(i[0])
        return top_words[:top_n]
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
    requirements=[isinstance(tokens,list),isinstance(word,str),
                  isinstance(left_context_size,int), isinstance(right_context_size,int),
                  not isinstance(left_context_size,bool),not isinstance(right_context_size,bool)]
    if all (requirements):
        concordance = []
        for i, el in enumerate(tokens):
            if el == word:
                word_index = i
                if left_context_size > 0 and right_context_size > 0:
                    concordance.append(tokens[word_index - left_context_size:word_index + 1 + right_context_size])
                elif left_context_size > 0:
                    concordance.append(tokens[word_index - left_context_size:word_index+1])
                elif right_context_size > 0:
                    concordance.append(tokens[word_index:word_index + right_context_size + 1])
        return concordance
    return []

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
    requirements = [isinstance(tokens, list), isinstance(word, str), isinstance(left_n, int),
                    isinstance(right_n, int),
                    not isinstance(left_n, bool), not isinstance(right_n, bool)]
    if all(requirements):
        adjacent_words=[]
        conc=get_concordance(tokens,word,left_n,right_n)
        for i in conc:
            if left_n>0 and right_n>0:
                adjacent_words.append([i[0],i[-1]])
            elif right_n>0:
                adjacent_words.append([i[-1]])
            elif left_n>0:
                adjacent_words.append([i[0]])
        return adjacent_words
    return []



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
    with open (path_to_file,"w",encoding="utf-8") as fs:
        fs.write(" ".join(content))


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
