"""
Longest common subsequence problem
"""
from tokenizer import tokenize

def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    if not isinstance(text, str):
        return ()
    result = []
    text = text.split('.')
    for sent in text:
        sent = tuple(tokenize(sent))
        if len(sent) > 0:
            result.append(sent)
    return tuple(result)
    



def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not isinstance(rows, int) or not isinstance(columns, int) or (isinstance(rows, bool) or isinstance(columns, bool)):
        return []
    elif rows < 1 or columns < 1:
        return []
    return [[0 for _ in range(columns)] for _ in range(rows)]



def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple):
        return []
    if not len(first_sentence_tokens) > 0 or not len(second_sentence_tokens) > 0:
        return []
    if not isinstance(first_sentence_tokens[0], str) or not isinstance(second_sentence_tokens[0], str):
        return []
    rows = len(first_sentence_tokens)
    columns = len(second_sentence_tokens)
    matrix = create_zero_matrix(rows, columns)
    for row in range(rows):
        for column in range(columns):
            common = first_sentence_tokens[row] == second_sentence_tokens[column]
            matrix[row][column] = max(matrix[row-1][column], matrix[row][column-1])
            if common:
                matrix[row][column] += 1
    return matrix


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if matrix == []:
        if first_sentence_tokens == () or second_sentence_tokens == ():
            return 0
        else:
            return -1
    if not isinstance(plagiarism_threshold, float):
        return -1
    if plagiarism_threshold > 1 or plagiarism_threshold < 0:
        return -1
    if matrix[-1][-1] / len(second_sentence_tokens) >= plagiarism_threshold:
        return matrix[-1][-1]
    else:
        return 0


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    row = -1
    col = -1
    result = []
    given = [(first_sentence_tokens, tuple, str, str),
             (second_sentence_tokens, tuple, str, str),
             (lcs_matrix, list, list, int)]
    for item in given:
        if not isinstance(item[0], item[1]):
            return ()
        if not len(item[0]) > 0:
            return ()
        if not isinstance(item[0][0], item[2]):
            return ()
        if not isinstance(item[0][0][0], item[3]):
            return ()
    if lcs_matrix[-1][-1] == 0 or not(lcs_matrix[0][0] == 1 or lcs_matrix[0][0] == 0):
        return ()
    while abs(row) <= len(first_sentence_tokens) or abs(col) <= len(second_sentence_tokens):
        if abs(col - 1) <= len(second_sentence_tokens):
            if lcs_matrix[row][col] == lcs_matrix[row][col - 1]:
                col -= 1
                continue
        if abs(row - 1) <= len(first_sentence_tokens):
            if lcs_matrix[row][col] == lcs_matrix[row - 1][col]:
                row -= 1
                continue
        result.append(first_sentence_tokens[row])
        row -= 1
        col -= 1
    return tuple(result[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int) or not isinstance(suspicious_sentence_tokens, tuple):
        return float(-1)
    if None in suspicious_sentence_tokens or isinstance(lcs_length, bool):
        return float(-1)
    for token in suspicious_sentence_tokens:
        if not isinstance(token, str):
            return float(-1)
    lentokens = len(suspicious_sentence_tokens)
    if lentokens == 0:
        return float(0)
    plagiarism_score = lcs_length / lentokens
    if not (0 <= plagiarism_score <= 1):
        return float(-1)
    return plagiarism_score


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple, plagiarism_threshold = 0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return float(-1)
    if not original_text_tokens or not suspicious_text_tokens:
        return float(-1)
    for sent in original_text_tokens:
        if not isinstance(sent, tuple):
            return float(-1)
        for word in sent:
            if not isinstance(word, str):
                return float(-1)
    for sent in suspicious_text_tokens:
        if not isinstance(sent, tuple):
            return float(-1)
        for word in sent:
            if not isinstance(word, str):
                return float(-1)
    len1 = len(original_text_tokens)
    len2 = len(suspicious_text_tokens)
    if len1 < len2:
        original_text_tokens += (() * (len2 - len1))
    elif len2 < len1:
        original_text_tokens = original_text_tokens[:len2]
    summ = 0
    for sent in range(len(original_text_tokens)):
        lcs_length = find_lcs_length(original_text_tokens[sent], suspicious_text_tokens[sent], plagiarism_threshold)
        if lcs_length == float(-1):
            return float(-1)
        p_sent = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[sent])
        if p_sent == -1:
            p_sent = 0.
        summ += p_sent
    result = summ / len(suspicious_text_tokens)
    return result

@unittest.skip('')
def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    pass

@unittest.skip('')
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
    pass

@unittest.skip('')
def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    pass

@unittest.skip('')
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

@unittest.skip('')
def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    pass

