import re
def tokenize(text: str) -> list:
    """
        Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
        :param text: the initial text
        :return: a list of lowercased tokens without punctuation
        e.g. text = 'The weather is sunny, the man is happy.'
        --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
        """
    if isinstance(text,str): #проверяем, строка ли это
        return []
    text = re.sub(r'[^A-Za-z 0-9]', '', text) # с помощью рег. выраж. убираю знаки препинания и числительные
    tokenize_list = text.split().lower()
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

    if isinstance(tokenize_list, list) and isinstance(stop_words, list):#проверяем, списки ли это
        return []
        for token in stop_words:
            if token not in stop_words: #проверяем входит ли слово в список стоп-слов
                tokenize_list.append(token)
            return tokenize_list



def calculate_frequencies(tokens: list) -> dict:
    """
        Calculates frequencies of given tokens
        :param tokens: a list of tokens without stop words
        :return: a dictionary with frequencies
        e.g. tokens = ['weather', 'sunny', 'man', 'happy']
        --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
        """
    if isinstance(tokenize_list, list):
        return {}
    dict = {} #создаем словарь
    for token in tokenize_list:
        if token in dict:
            dict[token] += 1
        else:
            dict[token] = 1
    return dict



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
    if isinstance(freq_dict, dict) and isinstance(top_n, int): #проверяем
        list_dict_items = list(freq_dict.items())
        list_dict_items.sort(key=lambda x: x[1], reverse=True)
        top_n = []
        if top_n > len(list_dict_items):
            return []
        else:
            for word in list_dict_items[:top_n]:
                top_n.append(word[0])
    return top_n



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
    if isinstance(tokens, list) and isinstance(word, str) and isinstance(left_context_size, int) and isinstance(right_context_size,int):
        concordance = []
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
    if isinstance(tokens, list) and isinstance(word, str) and isinstance(left_n, int) and isinstance(right_n, int)/n
    and (left_n < 1) and (right_n < 1):
        previous_conc = get_concordance(tokens, word, left_n, right_n)
        ad_word = []
        for cotext in previous_conc:
            if (left_n < 1) and (right_n >= 1):
                ad_word.append([previous_conc[-1]])
            elif (right_n < 1) and (left_n >= 1):
                ad_word.append([previous_conc[0]])
            elif (right_n >= 1) and (left_n >= 1):
                ad_word.append([previous_conc[0]], [previous_conc[-1]])
        return  ad_word



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
        for i in content:
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
