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
    if not isinstance(text, str):
        return ()

    text = text.split('\n')
    text_tuple = ()
    for sentence in text:
        clear_sentence = tokenize(sentence)
        if not clear_sentence:
            continue
        text_tuple += (tuple(clear_sentence),)
    return text_tuple


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """

    check = (isinstance(rows, int) and isinstance(columns, int) and
             (rows > 0) and (columns > 0) and not isinstance(rows, bool) and not isinstance(columns, bool))
    if not check:
        return []

    new_matrix = [[0] * columns for _ in range(rows)]
    return new_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """

    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or\
            not len(first_sentence_tokens) or not len(second_sentence_tokens) or\
            not isinstance(first_sentence_tokens[0], str) or not isinstance(second_sentence_tokens[0], str):
        return []

    matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    last = 0
    for row_i, row_element in enumerate(first_sentence_tokens):
        for column_i, column_element in enumerate(second_sentence_tokens):
            if row_element == column_element and row_i < len(second_sentence_tokens):
                matrix[row_i][column_i] = matrix[row_i - 1][column_i - 1] + 1
                last = matrix[row_i - 1][column_i - 1] + 1
            else:
                if row_i > len(second_sentence_tokens) - 1:
                    matrix[row_i][column_i] = last
                else:
                    matrix[row_i][column_i] = max((matrix[row_i][column_i - 1], matrix[row_i - 1][column_i]))
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
    if not matrix:
        if first_sentence_tokens == () or second_sentence_tokens == ():
            return 0
        return -1

    if not isinstance(plagiarism_threshold, float):
        return -1

    if plagiarism_threshold > 1 or plagiarism_threshold < 0:
        return -1

    if matrix[-1][-1]/len(second_sentence_tokens) >= plagiarism_threshold:
        return matrix[-1][-1]
    return 0


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    check = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)
             or not isinstance(lcs_matrix, list))
    check2 = not first_sentence_tokens or not second_sentence_tokens or not lcs_matrix

    if check or check2:
        return ()

    if (len(lcs_matrix) != len(first_sentence_tokens)) or (len(lcs_matrix[0]) != len(second_sentence_tokens)) or \
            (lcs_matrix[0][0] > 1):
        return ()

    lcs = []
    for row_index, row in enumerate(reversed(lcs_matrix)):
        for column_index, column in enumerate(reversed(row)):
            if not row or not column:
                return ()
            if first_sentence_tokens[row_index] == second_sentence_tokens[column_index]:
                lcs.append(second_sentence_tokens[column_index])

    lcs = tuple(lcs)

    return lcs


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int) or isinstance(lcs_length, bool) or \
            not isinstance(suspicious_sentence_tokens, tuple) or \
            lcs_length < 0 or not all([isinstance(word, str) for word in suspicious_sentence_tokens]):
        return -1.0

    if len(suspicious_sentence_tokens) == 0:
        return 0.0

    if lcs_length > len(suspicious_sentence_tokens):
        return -1.0

    score = lcs_length / len(suspicious_sentence_tokens)
    return score


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
    check = (not isinstance(original_text_tokens, tuple)
             or not all(isinstance(i, tuple) for i in original_text_tokens)
             or not all(isinstance(i, str) for tokens in original_text_tokens for i in tokens))

    check2 = (not isinstance(suspicious_text_tokens, tuple)
              or not all(isinstance(i, tuple) for i in suspicious_text_tokens)
              or not all(isinstance(i, str) for tokens in suspicious_text_tokens for i in tokens))

    if check or check2:
        return -1.0

    if not isinstance(plagiarism_threshold, float) or not (0 < plagiarism_threshold < 1):
        return -1.0

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += ((),) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]
    plagiarism = 0
    for i in range(len(suspicious_text_tokens)):
        length = find_lcs_length(original_text_tokens[i], suspicious_text_tokens[i], plagiarism_threshold)
        plag_score = calculate_plagiarism_score(length, suspicious_text_tokens[i])
        plagiarism += plag_score
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
