"""
Longest common subsequence problem
"""
from lab_2.tokenizer import tokenize

def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    if not isinstance(text,str):
        return ()
    text = text.split('\n')
    result = tuple(tuple(tokenize(x)) for x in text if tokenize(x))
    return result



def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    check_type = [isinstance(rows,int) and isinstance(columns,int) and not isinstance(rows,bool) and not isinstance(columns,bool)]
    if not all(check_type) or not rows > 0 or not columns > 0:
        return []
    matrix = []
    for row_index in range(rows):
        matrix += [[0*i for i in range(columns)]]
    return matrix



def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens,tuple) or not isinstance(second_sentence_tokens, tuple)\
        or not all(isinstance(word,str) for word in first_sentence_tokens)\
        or not all(isinstance(word,str) for word in second_sentence_tokens):
        return []
    lcs_matrix = create_zero_matrix(len(first_sentence_tokens),len(second_sentence_tokens))
    for index_1 in range(len(first_sentence_tokens)):
        for index_2 in range(len(second_sentence_tokens)):
            if first_sentence_tokens[index_1] == second_sentence_tokens[index_2] and index_1 == index_2:
                if lcs_matrix[index_1-1][index_2-1] >= 0:
                    cell = lcs_matrix[index_1-1][index_2-1]+1
                else:
                    cell = 1
            else:
                if index_2 >= 0 and index_1 >= 0:
                    cell = max(lcs_matrix[index_1][index_2-1], lcs_matrix[index_1-1][index_2])
                elif not index_2 >= 0 and not index_1 >= 0:
                    cell = 0
            lcs_matrix[index_1][index_2] = cell
    return lcs_matrix



def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    lcs_matrix = fill_lcs_matrix(first_sentence_tokens,second_sentence_tokens)
    check_type = [isinstance(plagiarism_threshold,float), isinstance(first_sentence_tokens,tuple),
                  isinstance(second_sentence_tokens, tuple)]
    check_type_2 = False
    if all(check_type):
        check_type_2 = [all(isinstance(word, str) for word in second_sentence_tokens),
                        all(isinstance(word, str) for word in first_sentence_tokens),
                        plagiarism_threshold >= 0, plagiarism_threshold <= 1]
    if all(check_type) and all(check_type_2) and\
            (len(second_sentence_tokens) == 0 or len(lcs_matrix) / len(second_sentence_tokens) < plagiarism_threshold):
        return 0
    if not all(check_type) or not all(check_type_2):
        return -1
    return lcs_matrix[-1][-1]


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    lcs_matrix_right = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    check_sentence = [isinstance(first_sentence_tokens,tuple),isinstance(second_sentence_tokens, tuple),
                      first_sentence_tokens, second_sentence_tokens]
    if not all(check_sentence) or lcs_matrix != lcs_matrix_right:
        return ()
    index_1 = len(first_sentence_tokens) - 1
    index_2 = len(second_sentence_tokens) - 1
    lcs = []
    while len(lcs) != lcs_matrix[-1][-1] and index_1 >= 0 and index_2 >= 0:
        if index_1 > 0:
            cell_1 = lcs_matrix[index_1-1][index_2]
        if index_2 > 0:
            cell_2 = lcs_matrix[index_1][index_2-1]
        if index_1 != 0 and index_2 == 0:
            index_1 = 0
        if first_sentence_tokens[index_1] == second_sentence_tokens[index_2]:
            lcs.append(first_sentence_tokens[index_1])
            index_1 -= 1
            index_2 -= 1
        elif cell_1 > cell_2:
            index_1 -= 1
        else:
            index_2 -= 1
        lcs.reverse()
    return tuple(lcs)


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    check_type = [isinstance(lcs_length, int), isinstance(suspicious_sentence_tokens, tuple)]
    if all(check_type) and not suspicious_sentence_tokens:
        return 0.0
    if  not all(check_type) or not all(isinstance(word, str) for word in suspicious_sentence_tokens) or\
        isinstance(lcs_length, bool) or lcs_length < 0 or lcs_length > len(suspicious_sentence_tokens):
        return -1.0
    return lcs_length / len(suspicious_sentence_tokens)




def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple, plagiarism_threshold=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    check_type = [isinstance(original_text_tokens,tuple), isinstance(suspicious_text_tokens, tuple),
                  isinstance(plagiarism_threshold, float)]
    check_type_2 = []
    if all(check_type):
        check_type_2 = [all(isinstance(sentence, tuple) for sentence in original_text_tokens),
                        all(isinstance(sentence, tuple) for sentence in suspicious_text_tokens),
                        plagiarism_threshold >= 0, plagiarism_threshold <= 1]
    if not all(check_type) or not all(check_type_2):
        return -1.0
    plagiarism = 0.0
    if len(original_text_tokens) < len(suspicious_text_tokens):
        list_original = list(original_text_tokens)
        list_original.append([[]]* (len(suspicious_text_tokens)-len(original_text_tokens)))
        original_text_tokens = tuple(list_original)
    for index, sentence in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[index], sentence, plagiarism_threshold)
        plagiarism += calculate_plagiarism_score(lcs_length, sentence)
    return plagiarism / len(suspicious_text_tokens)




def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    check_type = [isinstance(original_sentence_tokens,tuple), isinstance(suspicious_sentence_tokens, tuple),
                  isinstance(lcs, tuple)]
    check_type_2 = []
    if all(check_type):
        check_type_2 = [all(isinstance(word, str) for word in original_sentence_tokens),
                        all(isinstance(word, str) for word in suspicious_sentence_tokens),
                        all(isinstance(word, str) for word in lcs)]
    if not all(check_type) or not all(check_type_2):
        return ()
    diff_index_original = []
    diff_index_suspicious = []
    for index, word in enumerate(original_sentence_tokens):
        if word not in lcs and (index == 0 or original_sentence_tokens[index - 1] in lcs):
            diff_index_original.append(index)
        if word not in lcs and (index == len(original_sentence_tokens) - 1 or original_sentence_tokens[index + 1] in lcs):
            diff_index_original.append(index + 1)
    for index, word in enumerate(suspicious_sentence_tokens):
        if word not in lcs and (index == 0 or suspicious_sentence_tokens[index - 1] in lcs):
            diff_index_suspicious.append(index)
        if word not in lcs and (index == len(suspicious_sentence_tokens) - 1 or suspicious_sentence_tokens[index + 1] in lcs):
            diff_index_suspicious.append(index + 1)
    diff_index = tuple(diff_index_original), tuple(diff_index_suspicious)
    return diff_index

def accumulate_diff_stats(original_text_tokens: tuple, suspicious_text_tokens: tuple, plagiarism_threshold=0.3) -> dict:
    """
    Accumulates the main statistics for pairs of sentences in texts:
            lcs_length, plagiarism_score and indexes of differences
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :return: a dictionary of main statistics for each pair of sentences
    including average text plagiarism, sentence plagiarism for each sentence and lcs lengths for each sentence
    {'text_plagiarism': int,
     'sentence_plagiarism': list,
     'sentence_lcs_length': list,
     'difference_indexes': list}
    """
    check_type = [isinstance(original_text_tokens, tuple), isinstance(suspicious_text_tokens, tuple),
                  isinstance(plagiarism_threshold, float)]
    check_type_2 = []
    if all(check_type):
        check_type_2 = [all(isinstance(sentence, tuple) for sentence in original_text_tokens),
                        all(isinstance(sentence, tuple) for sentence in suspicious_text_tokens),
                        plagiarism_threshold >= 0, plagiarism_threshold <= 1]
    if not all(check_type) or not all(check_type_2):
        return {}
    diff_stat = {}
    diff_stat['text_plagiarism'] = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    sentence_plagiatism = []
    sentence_lcs_length = []
    difference_indexes = []
    for index in range(len(suspicious_text_tokens)):
        lcs_length = find_lcs_length(original_text_tokens[index], suspicious_text_tokens[index], plagiarism_threshold)
        sentence_lcs_length.append(lcs_length)
        sentence_plagiatism.append(calculate_plagiarism_score(lcs_length, suspicious_text_tokens[index]))
        lcs_matrix = fill_lcs_matrix(original_text_tokens[index], suspicious_text_tokens[index])
        lcs = find_lcs(original_text_tokens[index], suspicious_text_tokens[index], lcs_matrix)
        difference_indexes.append(find_diff_in_sentence(original_text_tokens[index], suspicious_text_tokens[index], lcs))
    diff_stat['sentence_plagiarism'] = sentence_plagiatism
    diff_stat['sentence_lcs_length'] = sentence_lcs_length
    diff_stat['difference_indexes'] = difference_indexes
    return diff_stat



def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    pass


def find_lcs_length_optimized(first_sentence_tokens: tuple, second_sentence_tokens: tuple,
                              plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using an optimized algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    pass


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    pass
