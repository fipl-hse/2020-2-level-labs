"""
Longest common subsequence problem
"""
from tokenizer import tokenize


def checker(object_to_check, expected_type):
    expectations = [False]
    if expected_type is int and isinstance(object_to_check, int):
        expectations = [object_to_check >= 0,
                        object_to_check is not True]
    elif expected_type is tuple and isinstance(object_to_check, tuple):
        first_expectations = [not(isinstance(object_to_check, bool)),
                              object_to_check is not None,
                              not("" in object_to_check and len(object_to_check) == 1)]
        if first_expectations:
            if None not in object_to_check:
                expectations = [None not in [item for subtuple in object_to_check for item in subtuple]]
            else:
                expectations = [False]
        else:
            expectations = [False]

    elif expected_type is float and isinstance(object_to_check, float):
        expectations = [object_to_check is not True,
                        0 < object_to_check <= 1]
    elif expected_type is list and isinstance(object_to_check, list):
        first_expectations = [
                        object_to_check is not True,
                        object_to_check is not None,
                        ]
        if first_expectations:
            if None not in object_to_check:
                expectations = [None not in [item for sublist in object_to_check for item in sublist]]
            else:
                expectations = [False]
    if all(expectations):
        return True
    return False


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not checker(rows, int) or not checker(columns, int):
        return []
    return [[0] * columns for _ in range(rows)]


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not checker(first_sentence_tokens, tuple) or not checker(second_sentence_tokens, tuple):
        return []

    rows, columns = len(first_sentence_tokens), len(second_sentence_tokens)
    matrix = create_zero_matrix(rows, columns)

    for index_first, element_first in enumerate(first_sentence_tokens):
        for index_second, element_second in enumerate(second_sentence_tokens):
            if element_first == element_second:
                matrix[index_first][index_second] = matrix[index_first - 1][index_second - 1] + 1
            elif element_second != element_first:
                matrix[index_first][index_second] = max(matrix[index_first][index_second - 1],
                                                        matrix[index_first - 1][index_second])

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
    conditions = [checker(first_sentence_tokens, tuple),
                  checker(second_sentence_tokens, tuple),
                  isinstance(plagiarism_threshold, float)]
    if not all(conditions) or plagiarism_threshold > 1 or plagiarism_threshold < 0:
        return -1
    elif len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return 0

    matrix_tokens = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    index_row, index_column = len(matrix_tokens), len(matrix_tokens[0])
    length = matrix_tokens[index_row - 1][index_column - 1]

    if length / len(second_sentence_tokens) < plagiarism_threshold:
        return 0

    return length


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    lcs = []
    # conditions to find the subsequence
    conditions = [checker(lcs_matrix, list),
                  checker(first_sentence_tokens, tuple),
                  checker(second_sentence_tokens, tuple)]
    if not lcs_matrix or not all(conditions):
        return ()
    elif not len(lcs_matrix[0]) == len(second_sentence_tokens) and not len(lcs_matrix) == len(first_sentence_tokens):
        return ()

    row, column = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1
    while row >= 0:
        if column <= 0:# условие на перемещение
            row -= 1

        if first_sentence_tokens[row] == second_sentence_tokens[column]:
            lcs.append(first_sentence_tokens[row])

            row -= 1
            column -= 1
        elif lcs_matrix[row - 1][column] > lcs_matrix[row][column - 1]:
            row -= 1
        else:
            if column != 0:
                column -= 1

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

    conditions = [checker(lcs_length, int),
                  checker(suspicious_sentence_tokens, tuple)]
    if not all(conditions):
        return -1
    if lcs_length != 0 and len(suspicious_sentence_tokens) == 0:
        return 0.0
    if lcs_length == 0 and len(suspicious_sentence_tokens) == 0:
        return -1
    if not(lcs_length <= len(suspicious_sentence_tokens)):
        return -1
    if lcs_length == 0:
        return 0.0

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

    # checking the conditions
    conditions = [checker(original_text_tokens, tuple),
                  checker(suspicious_text_tokens, tuple),
                  checker(plagiarism_threshold, float)]

    if not all(conditions):
        return -1.0

    # preparation to count the score
    if len(original_text_tokens) < len(suspicious_text_tokens):
        changed_sent_tokens = list(original_text_tokens)
        for i in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            changed_sent_tokens.append(())
        original_text_tokens = tuple(changed_sent_tokens)
    elif len(suspicious_text_tokens) < len(original_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]

    lcs = 0
    # counting
    for l in range(len(original_text_tokens)):
        lcs_length = find_lcs_length(original_text_tokens[l], suspicious_text_tokens[l], plagiarism_threshold)
        lcs += calculate_plagiarism_score(lcs_length, suspicious_text_tokens[l])

    # decision about the score
    p_result = lcs / len(original_text_tokens)
    if p_result < plagiarism_threshold:
        return 0.0
    return p_result


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    conditions = [checker(original_sentence_tokens, tuple),
                  checker(suspicious_sentence_tokens, tuple),
                  checker(lcs, tuple)]
    if not(all(conditions)):
        return ()

    def count_difference(tokens):
        differences = []
        word_index = 0
        while word_index < len(tokens):
            if tokens[word_index] not in lcs:
                if word_index + 1 == len(tokens) or tokens[word_index + 1] in lcs:
                    differences.append(word_index)
                    differences.append(word_index + 1)
                    word_index += 1
                elif tokens[word_index + 1] not in lcs:
                    first_unmatch = word_index
                    second_unmatch = word_index
                    while second_unmatch != len(tokens) - 1 and \
                            tokens[second_unmatch + 1] not in lcs:
                        second_unmatch += 1
                    differences.append(first_unmatch)
                    differences.append(second_unmatch + 1)
                    word_index = second_unmatch + 1
            else:
                word_index += 1

        return tuple(differences)
    result = (count_difference(original_sentence_tokens), count_difference(suspicious_sentence_tokens))
    return result


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
    length = len(original_text_tokens)
    sentence_lcs_length = [find_lcs_length(original_text_tokens[sent], suspicious_text_tokens[sent], plagiarism_threshold)
                           for sent in range(length)]

    sentence_plagiarism = [calculate_plagiarism_score(length, suspicious_text_tokens[sent])
                           for length, sent in zip(sentence_lcs_length, range(length))]
    matrixes = [fill_lcs_matrix(original_text_tokens[sent], suspicious_text_tokens[sent])
                for sent in range(len(original_text_tokens))]
    sentence_lcs = [find_lcs(original_text_tokens[sent], suspicious_text_tokens[sent], matrix)
                    for sent, matrix in zip(range(length), matrixes)]
    difference_indexes = [find_diff_in_sentence(original_text_tokens[sent], suspicious_text_tokens[sent], lcs_one)
                          for sent, lcs_one in zip(range(len(original_text_tokens)), sentence_lcs)]

    text_score = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    return {'text_plagiarism': text_score,
            'sentence_plagiarism': sentence_plagiarism,
            'sentence_lcs_length': sentence_lcs_length,
            'difference_indexes': difference_indexes}


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    for sent_ind in range(len(original_text_tokens)):
        # here prepare the sentence
        print(f"+{original_text_tokens[sent_ind]}/n-{suspicious_text_tokens[sent_ind]}")
        print(f"lcs = {accumulated_diff_stats['sentence_lcs_length'][sent_ind]}, "
              f"plagiarism = {accumulated_diff_stats['sentence_plagiarism'][sent_ind]}")
    pass


def find_lcs_length_optimized(first_sentence_tokens: list, second_sentence_tokens: list) -> int:
    """
    Finds a length of the longest common subsequence using the Hirschberg's algorithm
    At the same time, if the first and last tokens coincide,
    they are immediately added to lcs and not analyzed
    :param first_sentence_tokens: a list of tokens
    :param second_sentence_tokens: a list of tokens
    :return: a length of the longest common subsequence
    """

    lcs = []
    # conditions to find the subsequence
    conditions = [
                  checker(first_sentence_tokens, tuple),
                  checker(second_sentence_tokens, tuple)]
    if not all(conditions):
        return ()

    row, column = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1
    while row >= 0:
        if column <= 0:  # условие на перемещение
            row -= 1

        if first_sentence_tokens[row] == second_sentence_tokens[column]:
            lcs.append(first_sentence_tokens[row])

            row -= 1
            column -= 1
        elif lcs_matrix[row - 1][column] > lcs_matrix[row][column - 1]:
            row -= 1
        else:
            if column != 0:
                column -= 1

    lcs.reverse()
    return tuple(lcs)