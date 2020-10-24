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
    return tuple(tuple(i.split()) for i in text.lower().replace('.', '').split('\n') if tuple(i.split()))

def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """

    check = [isinstance(rows, int) and isinstance(columns, int)
             and not isinstance(rows, bool) and not isinstance(columns, bool)]
    if not all(check) or rows < 1 or columns < 1:
        return []

    z_matrix = [[0] * columns for i in range(rows)]
    return z_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not all(isinstance(word, str) for word in first_sentence_tokens) \
            or not all(isinstance(word, str) for word in second_sentence_tokens):
        return []

    rows = len(first_sentence_tokens)
    cols = len(second_sentence_tokens)
    mtrx = create_zero_matrix(rows, cols)


    for row in range(rows):
        for col in range(cols):
            if first_sentence_tokens[row] == second_sentence_tokens[col]:
                lcs = mtrx[row - 1][col - 1] + 1 if row - 1 >= 0 and col - 1 >= 0 else 1
            else:
                left_cell = mtrx[row][col - 1] if col - 1 >= 0 else 0
                up_cell = mtrx[row - 1][col] if row - 1 >= 0 else 0
                lcs = max(left_cell, up_cell)
            mtrx[row][col] = lcs
    return mtrx


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """

    check_type = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or
                  not all(isinstance(i, str) for i in first_sentence_tokens) or
                  not all(isinstance(i, str) for i in second_sentence_tokens))

    check_plg_thr = not isinstance(plagiarism_threshold, float) or plagiarism_threshold < 0 or plagiarism_threshold > 1

    if check_type or check_plg_thr:
        return -1

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    lcs_length = 0

    if lcs_matrix:
        lcs_length = lcs_matrix[-1][-1]
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
    check_type = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)
                  or not isinstance(lcs_matrix, list))
    check_if_empty = not first_sentence_tokens or not second_sentence_tokens or not lcs_matrix

    if check_type or check_if_empty:
        return ()
    if (len(lcs_matrix) != len(first_sentence_tokens)) or (len(lcs_matrix[0]) != len(second_sentence_tokens)) or \
            (lcs_matrix[0][0] > 1):
        return ()

    lcs = []
    ind_r = len(first_sentence_tokens) - 1
    ind_c = len(second_sentence_tokens) - 1

    while ind_r >= 0 and ind_c >= 0:
        if first_sentence_tokens[ind_r] == second_sentence_tokens[ind_c]:
            lcs.append(first_sentence_tokens[ind_r])
            ind_r -= 1
            ind_c -= 1
        elif lcs_matrix[ind_r - 1][ind_c] > lcs_matrix[ind_r][ind_c - 1]:
            ind_r -= 1
        else:
            if ind_r == 1 or ind_c == 0:
                ind_r -= 1
            else:
                ind_c -= 1
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
    if not isinstance(suspicious_sentence_tokens, tuple):
        return -1.0
    if not suspicious_sentence_tokens or len(suspicious_sentence_tokens) == 0:
        return 0.0
    for token_from_sentence in suspicious_sentence_tokens:
        if not isinstance(token_from_sentence, str):
            return -1.0
    if not isinstance(lcs_length, int) or isinstance(lcs_length, bool) or lcs_length < 0:
        return -1.0
    if lcs_length > len(suspicious_sentence_tokens):
        return -1.0

    plagiarism_score = lcs_length / len(suspicious_sentence_tokens)
    return plagiarism_score


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
    check_orig = (not isinstance(original_text_tokens, tuple)
                      or not all(isinstance(i, tuple) for i in original_text_tokens)
                      or not all(isinstance(i, str) for tokens in original_text_tokens for i in tokens))

    check_susp = (not isinstance(suspicious_text_tokens, tuple)
                        or not all(isinstance(i, tuple) for i in suspicious_text_tokens)
                        or not all(isinstance(i, str) for tokens in suspicious_text_tokens for i in tokens))

    check_threshold = (not isinstance(plagiarism_threshold, float)
                       or not 0 < plagiarism_threshold < 1)

    if check_orig or check_susp or check_threshold:
        return -1

    if ((isinstance(original_text_tokens, tuple) and not any(original_text_tokens))
            or (isinstance(suspicious_text_tokens, tuple) and not any(suspicious_text_tokens))):
        return 0

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens = list(original_text_tokens)
        for _ in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    pl_result_sum = 0
    for i, suspicious_sentence in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[i], suspicious_sentence, plagiarism_threshold)
        pl_score = calculate_plagiarism_score(lcs_length, suspicious_sentence)
        pl_result_sum += pl_score

    text_plagiarism_score = pl_result_sum / len(suspicious_text_tokens)
    return text_plagiarism_score


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    orig_sent_type = not isinstance(original_sentence_tokens, tuple)
    susp_sent_type = not isinstance(suspicious_sentence_tokens, tuple)
    lcs_type = not isinstance(lcs, tuple)

    if orig_sent_type or susp_sent_type or lcs_type:
        return ()
    for function_parameter in (original_sentence_tokens, suspicious_sentence_tokens, lcs):
        if isinstance(function_parameter, tuple):
            if not all(isinstance(word, str) for word in function_parameter):
                return ()

    diff_sum = []
    sentences = (original_sentence_tokens, suspicious_sentence_tokens)

    for sentence in sentences:
        diff = []
        for i, token in enumerate(sentence):
            if token not in lcs:
                if i == 0 or sentence[i - 1] in lcs:
                    diff.append(i)
                if i == len(sentence) - 1 or sentence[i + 1] in lcs:
                    diff.append(i + 1)
        diff_sum.append(tuple(diff))

    return tuple(diff_sum)


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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) \
            or not isinstance(plagiarism_threshold, float) or 0 > plagiarism_threshold > 1:
        return {}

    diff_stats = {'text_plagiarism': 0, 'sentence_plagiarism': [], 'sentence_lcs_length': [],
                  'difference_indexes': []}

    diff_stats['text_plagiarism'] = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens,
                                                                    plagiarism_threshold)

    for original_sentence, suspicious_sentence in zip(original_text_tokens, suspicious_text_tokens):
        lcs_length = find_lcs_length(original_sentence, suspicious_sentence, plagiarism_threshold)
        diff_stats['sentence_lcs_length'].append(lcs_length)
        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_sentence)
        lcs_matrix = fill_lcs_matrix(original_sentence, suspicious_sentence)
        lcs = find_lcs(original_sentence, suspicious_sentence, lcs_matrix)
        sent_diff = find_diff_in_sentence(original_sentence, suspicious_sentence, lcs)
        if plagiarism_score == -1:
            plagiarism_score = 0
        diff_stats['sentence_plagiarism'].append(plagiarism_score)
        diff_stats['difference_indexes'].append(sent_diff)
    return diff_stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    check_type = (not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple))
    if check_type or not isinstance(accumulated_diff_stats, dict):
        return ''

    texts_length = len(original_text_tokens)
    result_stats = ''

    for sent_ind in range(texts_length):
        orig_sentence = list(original_text_tokens[sent_ind])
        susp_sentence = list(suspicious_text_tokens[sent_ind])
        difference_indexes = accumulated_diff_stats['difference_indexes'][sent_ind]

        insert_number = 0
        for index in difference_indexes[0]:
            orig_sentence.insert(index + insert_number, '|')
            susp_sentence.insert(index + insert_number, '|')
            insert_number += 1

        orig_sentence = ' '.join(orig_sentence)
        susp_sentence = ' '.join(susp_sentence)

        lcs = accumulated_diff_stats['sentence_lcs_length'][sent_ind]
        sentence_plagiarism = float(accumulated_diff_stats['sentence_plagiarism'][sent_ind] * 100)
        result_stats += '- {}\n+ {}\n\nlcs = {}, plagiarism = {}%\n\n'.format(orig_sentence,
                                                                              susp_sentence,
                                                                              lcs,
                                                                              sentence_plagiarism)
    text_plagiarism = float(accumulated_diff_stats['text_plagiarism'] * 100)
    result_stats += 'Text average plagiarism (words): {}%'.format(text_plagiarism)

    return result_stats


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
    return 0


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    return ()
