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
    if not isinstance(text, str) or not text:
        return ()
    sentences_list = text.split('\n')
    return tuple([tuple(tokenize(sentence)) for sentence in sentences_list if tokenize(sentence)])


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    check1 = not isinstance(rows, int) or isinstance(rows, bool)
    check2 = not isinstance(columns, int) or isinstance(columns, bool)
    if check1 or check2 or rows <= 0 or columns <= 0:
        return []
    return [[0 for _ in range(columns)] for _ in range(rows)]


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if (not isinstance(first_sentence_tokens, tuple) or
            not isinstance(second_sentence_tokens, tuple) or
            not all(isinstance(i, str) for i in first_sentence_tokens) or
            not all(isinstance(i, str) for i in second_sentence_tokens)):
        return []
    rows = len(first_sentence_tokens)
    cols = len(second_sentence_tokens)
    lcs_matrix = create_zero_matrix(rows, cols)
    for row in range(rows):
        for col in range(cols):
            if first_sentence_tokens[row] == second_sentence_tokens[col]:
                lcs = lcs_matrix[row-1][col-1] + 1 if row-1 >= 0 and col-1 >= 0 else 1
            else:
                left_cell = lcs_matrix[row][col-1] if col-1 >= 0 else 0
                top_cell = lcs_matrix[row-1][col] if row-1 >= 0 else 0
                lcs = max(left_cell, top_cell)
            lcs_matrix[row][col] = lcs
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
    check1 = (not isinstance(first_sentence_tokens, tuple) or
              not isinstance(second_sentence_tokens, tuple) or
              not all(isinstance(i, str) for i in first_sentence_tokens) or
              not all(isinstance(i, str) for i in second_sentence_tokens))
    check2 = (not isinstance(plagiarism_threshold, float) or
             plagiarism_threshold < 0 or
             plagiarism_threshold > 1)
    if check1 or check2:
        return -1
    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    lcs_length = lcs_matrix[-1][-1] if lcs_matrix else 0
    if lcs_length and lcs_length / len(second_sentence_tokens) < plagiarism_threshold:
        return 0
    return lcs_length


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    check1 = (not isinstance(first_sentence_tokens, tuple) or
              not isinstance(second_sentence_tokens, tuple) or
              not all(isinstance(i, str) for i in first_sentence_tokens) or
              not all(isinstance(i, str) for i in second_sentence_tokens))
    check2 = (not isinstance(lcs_matrix, list) or
              not lcs_matrix or
              not all(isinstance(i, list) for i in lcs_matrix) or
              not all(isinstance(i, int) for sublist in lcs_matrix for i in sublist) or
              all(isinstance(i, bool) for sublist in lcs_matrix for i in sublist))
    if check1 or check2 or not(lcs_matrix[0][0] == 0 or lcs_matrix[0][0] == 1):
        return ()
    lcs_list = []
    row = len(lcs_matrix) - 1
    col = len(lcs_matrix[0]) - 1
    while len(lcs_list) != lcs_matrix[-1][-1]:
        top_cell = lcs_matrix[row-1][col] if row-1 >= 0 else 0
        left_cell = lcs_matrix[row][col-1] if col-1 >= 0 else 0
        if first_sentence_tokens[row] == second_sentence_tokens[col]:
            lcs_list.append(first_sentence_tokens[row])
            row -= 1
            col -= 1
        elif top_cell > left_cell:
            row -= 1
        else:
            col -= 1
    return tuple(lcs_list[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    pass


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
    pass


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
