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
    tokens = tuple([tuple(tokenize(sentence)) for sentence in sentence_list if len(tokenize(sentence))])

    return tokens


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    are_bools = isinstance(rows, bool) or isinstance(columns, bool)
    are_not_ints = not (isinstance(rows, int) and isinstance(columns, int))

    if are_bools or are_not_ints or rows <= 0 or columns <= 0:
        return []

    return [[0 for _ in range(columns)] for _ in range(rows)]


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    is_not_good_fst = not ((isinstance(first_sentence_tokens, tuple) and not first_sentence_tokens)
                           or (isinstance(first_sentence_tokens, tuple) and first_sentence_tokens
                               and first_sentence_tokens[0] is not None))

    is_not_good_sst = not ((isinstance(second_sentence_tokens, tuple) and not second_sentence_tokens)
                           or (isinstance(second_sentence_tokens, tuple) and second_sentence_tokens
                               and second_sentence_tokens[0] is not None))

    if is_not_good_fst or is_not_good_sst:
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
                if (ind_1 - 1) < 0 < (ind_2 - 1):
                    lcs_matrix[ind_1][ind_2] = lcs_matrix[ind_1][ind_2 - 1]

                elif (ind_2 - 1) < 0 < (ind_1 - 1):
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
                                 and (isinstance(plagiarism_threshold, (int, float)))
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
        for element in reversed(row):
            if element > max_el:
                are_good_matrix_els = False
                break

    if not are_good_matrix_els:
        return ()

    lcs = []

    ind_row, ind_col = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1

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

    is_not_good_sentence = not isinstance(suspicious_sentence_tokens, tuple)

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


def find_each_plag_score(original_text, suspicious_text):
    each_plag_score = []

    for ind_sent, sent_1 in enumerate(original_text):
        sent_2 = suspicious_text[ind_sent]
        lcs_length = find_lcs_length(sent_1, sent_2, 0)
        each_plag_score.append(calculate_plagiarism_score(lcs_length, sent_2))

    return each_plag_score


def make_sentences_same_lengths(original_text, length_orig_text, length_susp_text):
    if length_orig_text < length_susp_text:
        for _ in range(length_orig_text - length_susp_text):
            original_text += ()

    elif length_orig_text > length_susp_text:
        original_text = original_text[:length_susp_text]

    return original_text


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

    is_not_good_orig_text = not ((isinstance(original_text_tokens, tuple)
                                  and original_text_tokens
                                  and isinstance(original_text_tokens[0], tuple)
                                  and (not original_text_tokens[0]
                                       or (original_text_tokens[0] and isinstance(original_text_tokens[0][0], str)
                                           and original_text_tokens[0][0])))
                                 or (isinstance(original_text_tokens, tuple) and not original_text_tokens))

    is_not_good_susp_text = not ((isinstance(suspicious_text_tokens, tuple)
                                  and suspicious_text_tokens
                                  and isinstance(suspicious_text_tokens[0], tuple)
                                  and (not suspicious_text_tokens[0]
                                       or (suspicious_text_tokens[0] and isinstance(suspicious_text_tokens[0][0], str)
                                           and suspicious_text_tokens[0][0])))
                                 or (isinstance(suspicious_text_tokens, tuple) and not suspicious_text_tokens))

    is_not_good_plag_threshold = not (not isinstance(plagiarism_threshold, bool)
                                      and (isinstance(plagiarism_threshold, (float, int)))
                                      and 0 <= plagiarism_threshold <= 1)

    if is_not_good_orig_text or is_not_good_susp_text or is_not_good_plag_threshold:
        return -1.0

    length_orig_text = len(original_text_tokens)
    length_susp_text = len(suspicious_text_tokens)

    if length_orig_text != length_susp_text:
        original_text_tokens = make_sentences_same_lengths(original_text_tokens, length_orig_text, length_susp_text)

    each_plag_score = find_each_plag_score(original_text_tokens, suspicious_text_tokens)

    p_result = sum(each_plag_score) / len(suspicious_text_tokens)

    return p_result


def fill_indexes(sentence: tuple, lcs: tuple) -> tuple:
    indexes = []
    ind = ind_lcs = len_diff = start_seq = 0

    while ind < len(sentence):
        if ind_lcs >= len(lcs):
            indexes.extend([ind, len(sentence)])
            break

        if sentence[ind] != lcs[ind_lcs]:
            if len_diff:
                ind += 1
                len_diff += 1
            else:
                start_seq = ind
                indexes.append(ind)
                ind += 1
                len_diff += 1

        elif sentence[ind] == lcs[ind_lcs]:

            if len_diff:
                indexes.append(start_seq + len_diff)
                len_diff = 0

            ind += 1
            ind_lcs += 1

            while ind < len(sentence) and ind_lcs < len(lcs):
                if sentence[ind] == lcs[ind_lcs]:
                    ind += 1
                    ind_lcs += 1
                else:
                    break

    if len_diff:
        indexes.append(len(sentence))

    return tuple(indexes)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    is_not_good_orig_sentence = not ((isinstance(original_sentence_tokens, tuple) and not original_sentence_tokens)
                                     or (isinstance(original_sentence_tokens, tuple) and original_sentence_tokens
                                         and isinstance(original_sentence_tokens[0], str)))

    is_not_good_susp_sentence = not ((isinstance(suspicious_sentence_tokens, tuple) and not suspicious_sentence_tokens)
                                     or (isinstance(suspicious_sentence_tokens, tuple) and suspicious_sentence_tokens
                                         and isinstance(suspicious_sentence_tokens[0], str)))

    is_not_good_lcs = not ((isinstance(lcs, tuple) and not lcs)
                           or (isinstance(lcs, tuple) and lcs
                               and isinstance(lcs[0], str)))

    if is_not_good_orig_sentence or is_not_good_susp_sentence or is_not_good_lcs:
        return ()

    if not lcs:
        if original_sentence_tokens:
            first_sent = (0, len(original_sentence_tokens))
        else:
            first_sent = ()

        if suspicious_sentence_tokens:
            second_sent = (0, len(suspicious_sentence_tokens))
        else:
            second_sent = ()

        return first_sent, second_sent

    first_sent_inds = fill_indexes(original_sentence_tokens, lcs)
    second_sent_inds = fill_indexes(suspicious_sentence_tokens, lcs)

    return first_sent_inds, second_sent_inds


def find_each_diff_indexes(original_text, suspicious_text):
    indexes = []
    for i, sent_2 in enumerate(suspicious_text):
        sent_1 = original_text[i]

        lcs_matrix = fill_lcs_matrix(sent_1, sent_2)
        lcs = find_lcs(sent_1, sent_2, lcs_matrix)
        differences = find_diff_in_sentence(sent_1, sent_2, lcs)

        indexes.append(differences)

    return indexes


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

    orig_text_length = len(original_text_tokens)
    sus_text_length = len(suspicious_text_tokens)

    if orig_text_length != sus_text_length:
        original_text_tokens = make_sentences_same_lengths(original_text_tokens, orig_text_length, sus_text_length)

    stats_dict = {}

    stats_dict['text_plagiarism'] = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens,
                                                                    plagiarism_threshold)

    stats_dict['sentence_plagiarism'] = find_each_plag_score(original_text_tokens, suspicious_text_tokens)

    stats_dict['sentence_lcs_length'] = [find_lcs_length(original_text_tokens[i], suspicious_text_tokens[i],
                                                         plagiarism_threshold) for i in range(sus_text_length)]

    stats_dict['difference_indexes'] = find_each_diff_indexes(original_text_tokens, suspicious_text_tokens)

    return stats_dict


def add_lines(sent_1, sent_2, indexes):
    sent_1 = list(sent_1)
    sent_2 = list(sent_2)

    correction = 0
    for i in indexes[0]:
        sent_1.insert(i + correction, '|')
        correction += 1

    correction = 0
    for i in indexes[1]:
        sent_2.insert(i + correction, '|')
        correction += 1

    return ' '.join(sent_1), ' '.join(sent_2)


def form_output(report):
    output = ''
    for sent in report:
        output += f'''
- {sent[0][0]}
+ {sent[0][1]}

lcs = {sent[2]}, plagiarism = {sent[1] * 100}%
'''

    return output


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    is_not_good_orig_text = not isinstance(original_text_tokens, tuple)
    is_not_good_susp_text = not isinstance(suspicious_text_tokens, tuple)

    if is_not_good_orig_text or is_not_good_susp_text:
        return ''

    orig_text_length = len(original_text_tokens)
    susp_text_length = len(suspicious_text_tokens)

    if orig_text_length != susp_text_length:
        original_text_tokens = make_sentences_same_lengths(original_text_tokens, orig_text_length, susp_text_length)

    report_info = [[add_lines(original_text_tokens[i], suspicious_text_tokens[i],
                              accumulated_diff_stats['difference_indexes'][i])]
                   for i in range(susp_text_length)]

    total_plag_score = accumulated_diff_stats['text_plagiarism']

    del accumulated_diff_stats['text_plagiarism'], accumulated_diff_stats['difference_indexes']

    for info in accumulated_diff_stats.values():
        for i in range(susp_text_length):
            report_info[i].append(info[i])

    output = form_output(report_info) + f'\nText average plagiarism (words): {total_plag_score * 100}%'

    return output


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
    return


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    return
