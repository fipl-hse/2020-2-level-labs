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
    tokens_tuple = ()

    if not isinstance(text, str):
        return tokens_tuple

    lines_list = text.split('\n')
    tokens_list = []
    for line in lines_list:
        line_tuple = tuple(tokenizer.tokenize(line))
        if line_tuple:
            tokens_list.append(line_tuple)
    tokens_tuple = tuple(tokens_list)

    return tokens_tuple


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    zero_matrix = []

    input_check = [
        isinstance(rows, int),
        isinstance(columns, int),
        not isinstance(rows, bool),
        not isinstance(columns, bool),
    ]
    if not all(input_check):
        return zero_matrix
    if rows <= 0 or columns <= 0:
        return zero_matrix

    for _ in range(rows):
        matrix_row = [0] * columns
        zero_matrix.append(matrix_row)


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    matrix = []

    tokens_1, tokens_2 = first_sentence_tokens, second_sentence_tokens
    if not isinstance(tokens_1, tuple) or not isinstance(tokens_2, tuple):
        return matrix
    if not len(tokens_1) > 1 or not len(tokens_2) > 1:
        return matrix
    for token_1, token_2 in zip(tokens_1, tokens_2):
        if not isinstance(token_1, str) or not isinstance(token_2, str):
            return matrix

    matrix = create_zero_matrix(len(tokens_1), len(tokens_2))
    for index_1, token_1 in enumerate(tokens_1):
        for index_2, token_2 in enumerate(tokens_2):
            if token_1 == token_2:
                matrix[index_1][index_2] = matrix[index_1 - 1][index_2 - 1] + 1
            else:
                matrix[index_1][index_2] = max(matrix[index_1 - 1][index_2], matrix[index_1][index_2 - 1])

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
    lcs_length = -1
    tokens_1, tokens_2, threshold = first_sentence_tokens, second_sentence_tokens, plagiarism_threshold

    if not isinstance(tokens_1, tuple) or not isinstance(tokens_2, tuple) or not isinstance(threshold, float):
        return lcs_length
    if tokens_1 == () or tokens_2 == ():
        lcs_length = 0
        return lcs_length
    if threshold >= 1 or threshold <= 0 or not tokens_1 or not tokens_2:
        return lcs_length
    for token_1, token_2 in zip(tokens_1, tokens_2):
        if not isinstance(token_1, str) or not isinstance(token_2, str):
            return lcs_length
    if len(tokens_1) > len(tokens_2):
        tokens_1, tokens_2 = tokens_2, tokens_1

    matrix = fill_lcs_matrix(tokens_1, tokens_2)
    if not matrix:
        return lcs_length
    ratio = matrix[-1][-1] / len(tokens_2)
    lcs_length = matrix[-1][-1]
    if ratio < threshold:
        lcs_length = 0


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    lcs = ()
    tokens_1, tokens_2, matrix = first_sentence_tokens, second_sentence_tokens, lcs_matrix

    if not isinstance(tokens_1, tuple) or not isinstance(tokens_2, tuple) or not isinstance(matrix, list):
        return lcs
    if not tokens_1 or not tokens_2:
        return lcs
    if not matrix or len(matrix) != len(tokens_1) or len(matrix[0]) != len(tokens_2) or matrix[0][0] > matrix[-1][-1]:
        return lcs
    for token_1, token_2, matrix_row in zip(tokens_1, tokens_2, matrix):
        if not token_1 or not token_2 or not matrix_row:
            return lcs
        if not isinstance(token_1, str) or not isinstance(token_2, str):
            return lcs
        for elem in matrix_row:
            if not isinstance(elem, int) or isinstance(elem, bool) or elem < 0:
                return lcs

    lcs_list = []
    column_index, row_index = len(matrix[0]) - 1, len(matrix) - 1
    while len(lcs_list) != matrix[-1][-1]:
        upper_elem = matrix[row_index - 1][column_index] if row_index - 1 >= 0 else 0
        left_elem = matrix[row_index][column_index - 1] if column_index - 1 >= 0 else 0
        if tokens_1[row_index] == tokens_2[column_index]:
            lcs_list.append(tokens_1[row_index])
            row_index -= 1
            column_index -= 1
        elif upper_elem > left_elem:
            row_index -= 1
        else:
            column_index -= 1
    lcs_list.reverse()
    lcs = tuple(lcs_list)

    return lcs


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    plagiarism_score = -1.0

    if not isinstance(lcs_length, int) or isinstance(lcs_length, bool) \
            or not isinstance(suspicious_sentence_tokens, tuple):
        return plagiarism_score
    if not suspicious_sentence_tokens:
        plagiarism_score = 0.0
        return plagiarism_score
    else:
        if lcs_length < 0 or lcs_length > len(suspicious_sentence_tokens):
            return plagiarism_score
        for token in suspicious_sentence_tokens:
            if not isinstance(token, str):
                return plagiarism_score

    plagiarism_score = lcs_length / len(suspicious_sentence_tokens)

    return plagiarism_score


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple,
                                    plagiarism_threshold=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with togitkens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    plagiarism_score = -1.0

    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return plagiarism_score

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens_list = list(original_text_tokens)
        for empty in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_text_tokens_list.append('')
        original_text_tokens = tuple(original_text_tokens_list)
    scores_list = []
    for index, sentence in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[index], sentence, plagiarism_threshold)
        scores_list.append(calculate_plagiarism_score(lcs_length, sentence))
    scores_sum = 0.0
    for score in scores_list:
        scores_sum += score
    plagiarism_score = scores_sum / len(scores_list)

    return plagiarism_score


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    diff_indexes_tuple = ()

    if not isinstance(original_sentence_tokens, tuple) or not isinstance(suspicious_sentence_tokens, tuple) \
            or not isinstance(lcs, tuple):
        return diff_indexes_tuple
    if original_sentence_tokens and suspicious_sentence_tokens and lcs:
        for token_1, token_2, token_lcs in zip(original_sentence_tokens, suspicious_sentence_tokens, lcs):
            if not token_1 or not token_2 or not token_lcs:
                return diff_indexes_tuple
            if not isinstance(token_1, str) or not isinstance(token_2, str) or not isinstance(token_lcs, str):
                return diff_indexes_tuple

    diff_indexes_list = []
    sentences = (original_sentence_tokens, suspicious_sentence_tokens)
    for sentence in sentences:
        sub_diff_indexes = []
        for index, token in enumerate(sentence):
            if token not in lcs:
                if not index or sentence[index - 1] in lcs:
                    sub_diff_indexes.append(index)
                if index == len(sentence) - 1 or sentence[index + 1] in lcs:
                    sub_diff_indexes.append(index + 1)
        diff_indexes_list.append(tuple(sub_diff_indexes))
    diff_indexes_tuple = tuple(diff_indexes_list)

    return diff_indexes_tuple


def accumulate_diff_stats(original_text_tokens: tuple, suspicious_text_tokens: tuple,
                          plagiarism_threshold=0.3) -> dict:
    """
    Accumulates the main statistics for pairs of sentences in texts:
            lcs_length, plagiarism_score and indexes of differences
    :param plagiarism_threshold:
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :return: a dictionary of main statistics for each pair of sentences
    including average text plagiarism, sentence plagiarism for each sentence and lcs lengths for each sentence
    {'text_plagiarism': int,
     'sentence_plagiarism': list,
     'sentence_lcs_length': list,
     'difference_indexes': list}
    """
    diff_stats_dict = {}
    tokens_1, tokens_2, threshold = original_text_tokens, suspicious_text_tokens, plagiarism_threshold

    if not isinstance(tokens_1, tuple) or not isinstance(tokens_2, tuple):
        return diff_stats_dict
    if tokens_1 and tokens_2:
        for sentence_1, sentence_2 in zip(tokens_1, tokens_2):
            if not sentence_1 or not sentence_2:
                return diff_stats_dict

    if len(tokens_1) < len(tokens_2):
        tokens_1_list = list(tokens_1)
        for empty in range(len(tokens_2) - len(tokens_1)):
            tokens_1_list.append('')
        tokens_1 = tuple(tokens_1)
    diff_stats_dict['text_plagiarism'] = calculate_text_plagiarism_score(tokens_1, tokens_2, threshold)
    diff_stats_dict['sentence_plagiarism'] = []
    diff_stats_dict['sentence_lcs_length'] = []
    diff_stats_dict['difference_indexes'] = []
    for index, sentence in enumerate(tokens_2):
        length = find_lcs_length(tokens_1[index], sentence, threshold)
        diff_stats_dict['sentence_plagiarism'].append(calculate_plagiarism_score(length, sentence))
        diff_stats_dict['sentence_lcs_length'].append(length)
        diff_stats_dict['difference_indexes'].append(find_diff_in_sentence(tokens_1[index], sentence,
                                                                           find_lcs(tokens_1[index], sentence,
                                                                                    fill_lcs_matrix(tokens_1[index],
                                                                                                    sentence))))

    return diff_stats_dict


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    diff_report = ''
    tokens_1, tokens_2, stats = original_text_tokens, suspicious_text_tokens, accumulated_diff_stats

    if not isinstance(tokens_1, tuple) or not isinstance(tokens_2, tuple):
        return diff_report
    if tokens_1 and tokens_2:
        for sentence_1, sentence_2 in zip(tokens_1, tokens_2):
            if not sentence_1 or not sentence_2:
                return diff_report

    if len(tokens_1) < len(tokens_2):
        tokens_1_list = list(tokens_1)
        for empty in range(len(tokens_2) - len(tokens_1)):
            tokens_1_list.append('')
        tokens_1 = tuple(tokens_1)
    elif len(tokens_1) > len(tokens_2):
        tokens_1 = tokens_1[:len(tokens_2)]

    def add_lines(tokens, diff_index):
        for num in range(0, len(diff_index), 2):
            if diff_index[num] + 1 == diff_index[num + 1]:
                tokens[diff_index[num]] = '| ' + tokens[diff_index[num]] + ' |'
            else:
                tokens[diff_index[num]] = '| ' + tokens[diff_index[num]]
                tokens[diff_index[num + 1] - 1] = tokens[diff_index[num + 1] - 1] + ' |'
        return ' '.join(tokens)

    for sentence_index, (diff_index_1, diff_index_2) in enumerate(stats['difference_indexes']):
        tokens_1_list = list(tokens_1[sentence_index])
        tokens_2_list = list(tokens_2[sentence_index])
        lcs_length = stats['sentence_lcs_length'][sentence_index]
        plagiarism = stats['sentence_plagiarism'][sentence_index] * 100
        tokens_1_report = '- ' + add_lines(tokens_1_list, diff_index_1) + '\n'
        diff_report += tokens_1_report
        tokens_2_report = '+ ' + add_lines(tokens_2_list, diff_index_2) + '\n'
        diff_report += tokens_2_report
        lcs_plagiarism_report = '\nlcs = {}, plagiarism = {}\n\n'.format(lcs_length, plagiarism)
        diff_report += lcs_plagiarism_report
    final_report = 'Text average plagiarism (words): ' + str(stats['text_plagiarism'] * 100) + '%'
    diff_report += final_report

    return diff_report
  