"""
Longest common subsequence problem
"""

import tokenizer
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
    text_1 = text.split('\n')
    list = []
    for i in text_1:
        sen_list = tuple(tokenizer.tokenize(i))
        if sen_list:
            list.append(sen_list)
    return (tuple(list))

def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    requirments = [isinstance(rows, int), isinstance(columns, int), not isinstance(rows, bool),
                   not isinstance(columns, bool)]
    if all(requirments) and rows > 0 and columns > 0:
        matrix = []
        for row in range(rows):
            matrix.append([0 * i for i in range(columns)])
        return matrix
    return []

def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)\
            or None in first_sentence_tokens or None in second_sentence_tokens:
        return []
    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for row, el1 in enumerate(first_sentence_tokens):
        for col, el2 in enumerate(second_sentence_tokens):
            if el1 == el2:
                lcs_matrix[row][col] = lcs_matrix[row - 1][col - 1] + 1
            else:
                lcs_matrix[row][col] = max(lcs_matrix[row][col - 1], lcs_matrix[row - 1][col])
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
    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not isinstance(plagiarism_threshold, float) or None in first_sentence_tokens \
            or None in second_sentence_tokens or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1
    if lcs_matrix:
        length_lcs = lcs_matrix[-1][-1]
    else:
        return 0
    if (length_lcs / len(second_sentence_tokens)) < plagiarism_threshold:
        return 0
    return length_lcs


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if (not isinstance(first_sentence_tokens, tuple) or
            not isinstance(second_sentence_tokens, tuple) or
            not isinstance(lcs_matrix, list) or
            not lcs_matrix or
            not first_sentence_tokens or
            not second_sentence_tokens or
            len(lcs_matrix) != len(first_sentence_tokens) or
            len(lcs_matrix[0]) != len(second_sentence_tokens) or
            not lcs_matrix[0][0] == 0 or not lcs_matrix[0][0] == 1):
        return ()
    lcs_list = []
    for row, el1 in reversed(list(enumerate(first_sentence_tokens))):
        for col, el2 in reversed(list(enumerate(second_sentence_tokens))):
            if el1 == el2:
                lcs_list.append(el1)
                row, col = row - 1, col - 1
            else:
                if lcs_matrix[row - 1][col] > lcs_matrix[row][col - 1]:
                    row -= 1
                else:
                    col -= 1
    return tuple(reversed(lcs_list))

def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int) or isinstance(lcs_length, bool) or \
            not isinstance(suspicious_sentence_tokens, tuple) or None in suspicious_sentence_tokens:
        return -1
    if lcs_length > len(suspicious_sentence_tokens) and len(suspicious_sentence_tokens) > 0 or lcs_length < 0:
        return -1
    if not suspicious_sentence_tokens:
        plagiarism_score = 0.0
        return plagiarism_score
    plagiarism_score = lcs_length / len(suspicious_sentence_tokens)
    return plagiarism_score

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
    check_1 = (not isinstance(original_text_tokens, tuple)
                      or not all(isinstance(i, tuple) for i in original_text_tokens)
                      or not all(isinstance(i, str) for tokens in original_text_tokens for i in tokens))

    check_2 = (not isinstance(suspicious_text_tokens, tuple)
                        or not all(isinstance(i, tuple) for i in suspicious_text_tokens)
                        or not all(isinstance(i, str) for tokens in suspicious_text_tokens for i in tokens))

    check_3 = (not isinstance(plagiarism_threshold, float) or not (0 < plagiarism_threshold < 1))
    if check_1 or check_2 or check_3:
        return -1.0
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += ((),) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]
    plagiarism = 0
    for i in range(len(suspicious_text_tokens)):
        lcs_length = find_lcs_length(original_text_tokens[i], suspicious_text_tokens[i], plagiarism_threshold)
        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[i])
        plagiarism += plagiarism_score
    text_plagiarism = plagiarism / len(suspicious_text_tokens)
    return text_plagiarism

def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    pass


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
