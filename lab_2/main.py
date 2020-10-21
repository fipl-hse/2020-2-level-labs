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

    sentence_list = text.split('\n')
    tokens_list = [tuple(tokenize(sentence)) for sentence in sentence_list if len(tokenize(sentence))]

    return tuple(tokens_list)


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    is_bool_rows = isinstance(rows, bool)
    is_bool_columns = isinstance(columns, bool)
    is_not_int_rows = not isinstance(rows, int)
    is_not_int_columns = not isinstance(columns, int)

    if is_bool_rows or is_bool_columns or is_not_int_rows or is_not_int_columns or rows <= 0 or columns <= 0:
        return []

    return [[0 for _ in range(columns)] for _ in range(rows)]


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    is_not_tuple_fst = not isinstance(first_sentence_tokens, tuple)
    is_not_tuple_sst = not isinstance(second_sentence_tokens, tuple)

    if is_not_tuple_fst or is_not_tuple_sst or not first_sentence_tokens or not second_sentence_tokens or \
            (first_sentence_tokens and first_sentence_tokens[0] is None) or \
            (second_sentence_tokens and second_sentence_tokens[0] is None):
        return []

    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    for ind_1, elem_1 in enumerate(first_sentence_tokens):
        for ind_2, elem_2 in enumerate(second_sentence_tokens):
            if elem_1 == elem_2:
                if (ind_1 - 1) < 0 or (ind_2 - 1) < 0:
                    lcs_matrix[ind_1][ind_2] = 1
                else:
                    lcs_matrix[ind_1][ind_2] = lcs_matrix[ind_1 - 1][ind_2 - 1] + 1
            else:
                if (ind_1 - 1) < 0 and (ind_2 - 1) > 0:
                    #  (ind_2 - 1) < 0:
                    lcs_matrix[ind_1][ind_2] = lcs_matrix[ind_1][ind_2 - 1]
                elif (ind_1 - 1) > 0 and (ind_2 - 1) < 0:
                    lcs_matrix[ind_1][ind_2] = lcs_matrix[ind_1 - 1][ind_2]
                elif (ind_1 - 1) < 0 and (ind_2 - 1) < 0:
                    lcs_matrix[ind_1][ind_2] = 0
                else:
                    lcs_matrix[ind_1][ind_2] = max([lcs_matrix[ind_1][ind_2 - 1], lcs_matrix[ind_1 - 1][ind_2]])

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
    is_not_good_fst = not ((isinstance(first_sentence_tokens, tuple) and first_sentence_tokens
                            and first_sentence_tokens[0] is not None)
                           or (isinstance(first_sentence_tokens, tuple) and not first_sentence_tokens))

    is_not_good_sst = not ((isinstance(second_sentence_tokens, tuple) and second_sentence_tokens
                            and second_sentence_tokens[0] is not None)
                           or (isinstance(second_sentence_tokens, tuple) and not second_sentence_tokens))

    is_not_good_threshold = not (not isinstance(plagiarism_threshold, bool)
                                 and (isinstance(plagiarism_threshold, int) or isinstance(plagiarism_threshold, float))
                                 and 0 <= plagiarism_threshold <= 1)

    if is_not_good_fst or is_not_good_sst or is_not_good_threshold:
        return -1

    is_not_fst = not first_sentence_tokens
    is_not_sst = not second_sentence_tokens

    if is_not_fst or is_not_sst:
        return 0

    lcs_length = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)[-1][-1]

    if lcs_length / len(second_sentence_tokens) < plagiarism_threshold:
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
    is_not_good_fst = not (isinstance(first_sentence_tokens, tuple) and first_sentence_tokens
                           and first_sentence_tokens[0] is not None)
    is_not_good_sst = not (isinstance(second_sentence_tokens, tuple) and second_sentence_tokens
                           and second_sentence_tokens[0] is not None)

    if is_not_good_fst or is_not_good_sst:
        return ()

    is_not_good_lcs_matrix = not (isinstance(lcs_matrix, list) and lcs_matrix and isinstance(lcs_matrix[0], list)
                                  and isinstance(lcs_matrix[0][0], int) and lcs_matrix[0][0] >= 0
                                  and len(first_sentence_tokens) == len(lcs_matrix)
                                  and len(second_sentence_tokens) == len(lcs_matrix[0]))

    if is_not_good_lcs_matrix:
        return ()

    are_good_matrix_els = True
    max_el = lcs_matrix[-1][-1]
    for row in reversed(lcs_matrix):
        for el in reversed(row):
            if el > max_el:
                are_good_matrix_els = False
                break

    if not are_good_matrix_els:
        return ()

    lcs = []

    ind_row, ind_col = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1

    '''zero_row = [[0 for _ in range(len(lcs_matrix[0]))]]
    zero_row.extend(lcs_matrix)

    first_zero_el = []
    for row in lcs_matrix:
        new_row = [0]
        for el in row:
            new_row.append(el)
        first_zero_el.append(new_row)

    full_lcs_matrix = [[0 for _ in range(len(first_zero_el[0]))]]
    full_lcs_matrix.extend(first_zero_el)'''

    while ind_row >= 0 and ind_col >= 0:
        first_token, second_token = first_sentence_tokens[ind_row], second_sentence_tokens[ind_col]
        if first_token == second_token:
            lcs.append(first_token)
            ind_row, ind_col = ind_row - 1, ind_col - 1
        elif lcs_matrix[ind_row - 1][ind_col] > lcs_matrix[ind_row][ind_col - 1]:
            ind_row -= 1
        elif lcs_matrix[ind_row - 1][ind_col] == lcs_matrix[ind_row][ind_col - 1]:
            ind_row, ind_col = ind_row - 1, ind_col - 1
        else:
            ind_col -= 1

    if lcs_matrix[0][0] == 1 and len(lcs) == 0:
        lcs.append(first_sentence_tokens[0])

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

    is_not_good_sentence = not(isinstance(suspicious_sentence_tokens, tuple))

    if is_not_good_sentence:
        return -1

    are_not_good_tokens = False
    for token in suspicious_sentence_tokens:
        if not isinstance(token, str) and not token:
            are_not_good_tokens = True
            break

    if are_not_good_tokens:
        return -1

    if len(suspicious_sentence_tokens) == 0:
        return 0.0

    is_not_good_lcs_length = not (not isinstance(lcs_length, bool) and isinstance(lcs_length, int)
                                  and 0 <= lcs_length <= len(suspicious_sentence_tokens))

    if is_not_good_lcs_length:
        return -1

    return lcs_length / len(suspicious_sentence_tokens)


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple,
                                    plagiarism_threshold=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """

    is_not_good_orig_text = not((isinstance(original_text_tokens, tuple)
                                 and original_text_tokens
                                 and isinstance(original_text_tokens[0], tuple)
                                 and (not original_text_tokens[0]
                                      or (original_text_tokens[0] and isinstance(original_text_tokens[0][0], str)
                                      and original_text_tokens[0][0])))
                                or (isinstance(original_text_tokens, tuple) and not original_text_tokens))

    is_not_good_susp_text = not((isinstance(suspicious_text_tokens, tuple)
                                 and suspicious_text_tokens
                                 and isinstance(suspicious_text_tokens[0], tuple)
                                 and (not suspicious_text_tokens[0]
                                      or (suspicious_text_tokens[0] and isinstance(suspicious_text_tokens[0][0], str)
                                      and suspicious_text_tokens[0][0])))
                                or (isinstance(suspicious_text_tokens, tuple) and not suspicious_text_tokens))

    is_not_good_plag_threshold = not(not isinstance(plagiarism_threshold, bool)
                                     and (isinstance(plagiarism_threshold, float)
                                          or isinstance(plagiarism_threshold, int))
                                     and 0 <= plagiarism_threshold <= 1)

    if is_not_good_orig_text or is_not_good_susp_text or is_not_good_plag_threshold:
        return -1.0

    length_orig_text = len(original_text_tokens)
    length_susp_text = len(suspicious_text_tokens)

    if length_orig_text < length_susp_text:
        for i in range(length_orig_text - length_susp_text):
            original_text_tokens += ()

    elif length_orig_text > length_susp_text:
        original_text_tokens = original_text_tokens[:length_susp_text]

    each_plag_score = []

    for ind_sent, sent_1 in enumerate(original_text_tokens):
        sent_2 = suspicious_text_tokens[ind_sent]
        lcs_length = find_lcs_length(sent_1, sent_2, 0)
        each_plag_score.append(calculate_plagiarism_score(lcs_length, sent_2))

    p_result = sum(each_plag_score) / len(suspicious_text_tokens)

    return p_result


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
