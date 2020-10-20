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
    processed_text = tuple(tuple(tokenize(x)) for x in text if tokenize(x))
    return processed_text


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    rows_not_int = not isinstance(rows, int)
    columns_not_int = not isinstance(columns, int)
    columns_bool = isinstance(columns, bool)
    rows_bool = isinstance(rows, bool)
    if rows_bool or columns_bool or rows_not_int or columns_not_int or rows <= 0 or columns <= 0:
        return []
    zero_matrix = [[0] * columns for i in range(rows)]
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    frst_sent_not_t = not isinstance(first_sentence_tokens, tuple)
    scd_sent_not_t = not isinstance(second_sentence_tokens, tuple)
    if not frst_sent_not_t:
        if not all(isinstance(word, str) for word in first_sentence_tokens):
            return []
    if not scd_sent_not_t:
        if not all(isinstance(word, str) for word in second_sentence_tokens):
            return []
    if frst_sent_not_t or scd_sent_not_t:
        return []
    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for index_1, element_1 in enumerate(first_sentence_tokens):
        for index_2, element_2 in enumerate(second_sentence_tokens):
            if element_1 == element_2 and index_1 == index_2:
                lcs_matrix[index_1][index_2] = lcs_matrix[index_1 - 1][index_2 - 1] + 1
            else:
                lcs_matrix[index_1][index_2] = max(lcs_matrix[index_1][index_2 - 1], lcs_matrix[index_1 - 1][index_2])
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
    frst_sent_not_t = not isinstance(first_sentence_tokens, tuple)
    scd_sent_not_t = not isinstance(second_sentence_tokens, tuple)
    plagiarism_is_not_float = not isinstance(plagiarism_threshold, float)

    if not frst_sent_not_t:
        if not all(isinstance(word, str) for word in first_sentence_tokens):
            return -1
    if not scd_sent_not_t:
        if not all(isinstance(word, str) for word in second_sentence_tokens):
            return -1
    if frst_sent_not_t or scd_sent_not_t or plagiarism_is_not_float \
            or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1
    if not first_sentence_tokens or not second_sentence_tokens:
        return 0
    lcs_length = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)[-1][-1]
    if lcs_length/len(second_sentence_tokens) < plagiarism_threshold:
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

    frst_sent_not_t = not isinstance(first_sentence_tokens, tuple)
    scd_sent_not_t = not isinstance(second_sentence_tokens, tuple)
    matrix_not_lst = not isinstance(lcs_matrix, list)

    if not frst_sent_not_t:
        if not all(isinstance(word, str) for word in first_sentence_tokens):
            return ()
    if not scd_sent_not_t:
        if not all(isinstance(word, str) for word in second_sentence_tokens):
            return ()
    if frst_sent_not_t or scd_sent_not_t:
        return ()

    if matrix_not_lst or lcs_matrix == [] \
            or len(first_sentence_tokens) != len(lcs_matrix) \
            or len(second_sentence_tokens) != len(lcs_matrix[0])\
            or (lcs_matrix[0][0] != 0 and lcs_matrix[0][0] != 1):
        return ()

    lcs = []
    ind_r = len(first_sentence_tokens) - 1
    ind_c = len(second_sentence_tokens) - 1

    while ind_r >= 0 and ind_c >= 0:
        if first_sentence_tokens[ind_r] == second_sentence_tokens[ind_c]:
            lcs.append(first_sentence_tokens[ind_r])
            ind_r -= 1
            ind_c -= 1
        elif ind_r > ind_c:
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
    lcs_length_not_int = not isinstance(lcs_length, int)
    sus_sent_tokens_not_tuple = not isinstance(suspicious_sentence_tokens, tuple)
    if not sus_sent_tokens_not_tuple:
        if not all(isinstance(word, str) for word in suspicious_sentence_tokens):
            return -1
        if not suspicious_sentence_tokens:
            return 0.0

    if lcs_length_not_int or sus_sent_tokens_not_tuple or lcs_length > len(suspicious_sentence_tokens) \
            or lcs_length < 0 or type(lcs_length) == bool:
        return -1

    plagiarism_score = lcs_length/len(suspicious_sentence_tokens)
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
    orig_txt_not_tuple = not isinstance(original_text_tokens, tuple)
    sus_text_not_tuple = not isinstance(suspicious_text_tokens, tuple)
    plagiarism_not_float = not isinstance(plagiarism_threshold, float)
    if not orig_txt_not_tuple:
        for i in range(len(original_text_tokens)):
            if type(original_text_tokens[i]) == tuple:
                if not all(isinstance(word, str) for word in original_text_tokens[i]):
                    return -1.0
            else:
                return -1.0
    if not sus_text_not_tuple:
        for i in range(len(suspicious_text_tokens)):
            if type(suspicious_text_tokens[i]) == tuple:
                if not all(isinstance(word, str) for word in suspicious_text_tokens[i]):
                    return -1.0
            else:
                return -1.0
    if orig_txt_not_tuple or sus_text_not_tuple \
            or plagiarism_not_float or not (0 < plagiarism_threshold < 1):
        return -1.0

    original_list = list(original_text_tokens)
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_list.append(()*(len(suspicious_text_tokens) - len(original_text_tokens)))
    elif len(suspicious_text_tokens) < len(original_text_tokens):
        original_list = original_list[:len(suspicious_text_tokens)]
    original_text_tokens = tuple(original_list)

    p_result = 0
    for i in range(len(original_text_tokens)):
        length = find_lcs_length(original_text_tokens[i], suspicious_text_tokens[i], plagiarism_threshold)
        p_i = calculate_plagiarism_score(length, suspicious_text_tokens[i])
        p_result += p_i
    return p_result / len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    orig_sent_not_tuple = not isinstance(original_sentence_tokens, tuple)
    sus_sent_not_tuple = not isinstance(suspicious_sentence_tokens, tuple)
    lcs_not_tuple = not isinstance(lcs, tuple)
    if orig_sent_not_tuple or sus_sent_not_tuple or lcs_not_tuple:
        return ()
    if not orig_sent_not_tuple:
        if not all(isinstance(word, str) for word in original_sentence_tokens):
            return ()
    if not sus_sent_not_tuple:
        if not all(isinstance(word, str) for word in suspicious_sentence_tokens):
            return ()
    if not lcs_not_tuple:
        if not all(isinstance(word, str) for word in lcs):
            return ()

    org_dif_wds_ind = [original_sentence_tokens.index(word) for word in original_sentence_tokens if word not in lcs]
    sus_dif_wds_ind = [suspicious_sentence_tokens.index(word) for word in suspicious_sentence_tokens if word not in lcs]
    changed_ind_list = []

    changed_ind_list_1 = []
    if org_dif_wds_ind:
        ind = 0
        while ind < len(org_dif_wds_ind):
            if ind == len(org_dif_wds_ind) - 1:
                changed_ind_list_1.extend((org_dif_wds_ind[ind], org_dif_wds_ind[ind] + 1))
                break
            else:
                if org_dif_wds_ind[ind+1] - org_dif_wds_ind[ind] > 1:
                    changed_ind_list_1.extend((org_dif_wds_ind[ind], org_dif_wds_ind[ind] + 1))
                    ind += 1
                else:
                    changed_ind_list_1.append(org_dif_wds_ind[ind])
                    while org_dif_wds_ind[ind+1] - org_dif_wds_ind[ind] == 1:
                        ind += 1
                        if ind >= len(org_dif_wds_ind) - 1:
                            break
                    changed_ind_list_1.append(org_dif_wds_ind[ind] + 1)
                    ind += 1

    changed_ind_list_2 = []
    if sus_dif_wds_ind:
        ind = 0
        while ind < len(sus_dif_wds_ind):
            if ind == len(sus_dif_wds_ind) - 1:
                changed_ind_list_2.extend((sus_dif_wds_ind[ind], sus_dif_wds_ind[ind] + 1))
                break
            else:
                if sus_dif_wds_ind[ind + 1] - sus_dif_wds_ind[ind] > 1:
                    changed_ind_list_2.extend((sus_dif_wds_ind[ind], sus_dif_wds_ind[ind] + 1))
                    ind += 1
                else:
                    changed_ind_list_2.append(sus_dif_wds_ind[ind])
                    while sus_dif_wds_ind[ind + 1] - sus_dif_wds_ind[ind] == 1:
                        ind += 1
                        if ind >= len(sus_dif_wds_ind) - 1:
                            break
                    changed_ind_list_2.append(sus_dif_wds_ind[ind] + 1)
                    ind += 1

    changed_ind_list_1 = tuple(changed_ind_list_1)
    changed_ind_list_2 = tuple(changed_ind_list_2)
    changed_ind_list.extend((changed_ind_list_1, changed_ind_list_2))
    return tuple(changed_ind_list)


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
