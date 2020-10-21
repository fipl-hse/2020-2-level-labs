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
    if rows_bool or columns_bool or rows_not_int or columns_not_int:
        return []
    if rows <= 0 or columns <= 0:
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
            if element_1 == element_2:
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
    if len(first_sentence_tokens) > len(second_sentence_tokens):
        first_sentence_tokens = first_sentence_tokens[:len(second_sentence_tokens)]
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
            or len(second_sentence_tokens) != len(lcs_matrix[0]):
        return ()
    if lcs_matrix[0][0] != 0 and lcs_matrix[0][0] != 1:
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
    lcs_length_not_int = not isinstance(lcs_length, int)
    sus_sent_tokens_not_tuple = not isinstance(suspicious_sentence_tokens, tuple)
    if not sus_sent_tokens_not_tuple:
        if not all(isinstance(word, str) for word in suspicious_sentence_tokens):
            return -1
        if not suspicious_sentence_tokens:
            return 0.0

    if lcs_length_not_int or sus_sent_tokens_not_tuple or lcs_length > len(suspicious_sentence_tokens) \
            or lcs_length < 0 or isinstance(lcs_length, bool):
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

    # тут нужно в одно, исп enumerate
    for text_tokens in (original_text_tokens, suspicious_text_tokens):
        if isinstance(text_tokens, tuple):
            for ind, token in enumerate(text_tokens): # range(len(text_tokens)):
                if isinstance(token, tuple):
                    if not all(isinstance(word, str) for word in token):
                        return -1.0
                else:
                    return -1.0

    if orig_txt_not_tuple or sus_text_not_tuple \
            or plagiarism_not_float or 0 > plagiarism_threshold > 1:
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
    for function_parameter in (original_sentence_tokens, suspicious_sentence_tokens, lcs):
        if isinstance(function_parameter, tuple):
            if not all(isinstance(word, str) for word in function_parameter):
                return ()

    org_dif_wds_ind = [original_sentence_tokens.index(word) for word in original_sentence_tokens if word not in lcs]
    sus_dif_wds_ind = [suspicious_sentence_tokens.index(word) for word in suspicious_sentence_tokens if word not in lcs]
    changed_ind_list = []
    changed_ind_list_orig = []
    changed_ind_list_sus = []

    for data in ([org_dif_wds_ind, changed_ind_list_orig], [sus_dif_wds_ind, changed_ind_list_sus]):
        for ind, dif_wds_ind in enumerate(data[0]):
            if ind != len(data[0]) - 1:
                if dif_wds_ind + 1 != data[0][ind + 1]:
                    data[1].extend((dif_wds_ind, dif_wds_ind + 1))
                if dif_wds_ind - 1 != data[0][ind - 1] and dif_wds_ind + 1 == data[0][ind + 1]:
                    data[1].append(dif_wds_ind)
                if dif_wds_ind - 1 == data[0][ind - 1] and dif_wds_ind + 1 != data[0][ind + 1]:
                    data[1].append(dif_wds_ind + 1)
            if ind == len(data[0]) - 1:
                if dif_wds_ind - 1 != data[0][ind - 1]:
                    data[1].extend((dif_wds_ind, dif_wds_ind + 1))
                elif dif_wds_ind - 1 == data[0][ind - 1]:
                    data[1].append(dif_wds_ind + 1)

    if original_sentence_tokens == ():
        return tuple([(), tuple(changed_ind_list_sus)])
    if suspicious_sentence_tokens == ():
        return tuple([tuple(original_sentence_tokens), ()])

    changed_ind_list.extend((tuple(changed_ind_list_orig), tuple(changed_ind_list_sus)))
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

    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) \
            or not isinstance(plagiarism_threshold, float) or 0 > plagiarism_threshold > 1:
        return {}

    statistics = {'text_plagiarism': 0,
                  'sentence_plagiarism': [],
                  'sentence_lcs_length': [],
                  'difference_indexes': []}
    text_plagiarism = calculate_text_plagiarism_score(original_text_tokens,
                                                      suspicious_text_tokens,
                                                      plagiarism_threshold)
    statistics['text_plagiarism'] = text_plagiarism

    ind = 0
    while ind != len(original_text_tokens):
        sentence_lcs_length_i = find_lcs_length(original_text_tokens[ind],
                                                suspicious_text_tokens[ind],
                                                plagiarism_threshold)
        statistics['sentence_lcs_length'].append(sentence_lcs_length_i)
        sentence_plagiarism_i = calculate_plagiarism_score(sentence_lcs_length_i,
                                                           suspicious_text_tokens[ind])
        statistics['sentence_plagiarism'].append(sentence_plagiarism_i)
        lcs_matrix_i = fill_lcs_matrix(original_text_tokens[ind], suspicious_text_tokens[ind])
        lcs_i = find_lcs(original_text_tokens[ind], suspicious_text_tokens[ind], lcs_matrix_i)
        difference_indexes_i = find_diff_in_sentence(original_text_tokens[ind],
                                                     suspicious_text_tokens[ind],
                                                     lcs_i)
        statistics['difference_indexes'].append(difference_indexes_i)
        ind += 1
    return statistics

    # statistics = {'text_plagiarism': text_plagiarism,
    #               'sentence_plagiarism': sentence_plagiarism,
    #               'sentence_lcs_length': sentence_lcs_length,
    #               'difference_indexes': difference_indexes}
    # return statistics
    #убрать две переменные

def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    orig_text_not_tuple = not isinstance(original_text_tokens, tuple)
    sus_text_not_tuple = not isinstance(suspicious_text_tokens, tuple)
    diff_stats_not_dict = not isinstance(accumulated_diff_stats, dict)
    if orig_text_not_tuple or sus_text_not_tuple or diff_stats_not_dict:
        return ''
    report_data = accumulate_diff_stats(original_text_tokens, suspicious_text_tokens, plagiarism_threshold=0.3)

    ind = 0
    report = ""
    while ind != len(original_text_tokens):
        different_indexes = report_data['difference_indexes'][ind]
        report += "- "
        for index, word in enumerate(original_text_tokens[ind]):
            if index in different_indexes[0]:
                report += "| "
            report += "{} ".format(word)
        # if len(original_text_tokens[ind]) in different_indexes[0]:
        #     report += "|"
        report += "\n+ "
        for index, word in enumerate(suspicious_text_tokens[ind]):
            if index in different_indexes[1]:
                report += "| "
            report += "{} ".format(word)
        # if len(suspicious_text_tokens[ind]) in different_indexes[1]:
        #     report += "|"
        report += "\n\n"
        lcs_length = report_data['sentence_lcs_length'][ind]
        plagiarism = report_data['sentence_plagiarism'][ind] * 100
        report += "lcs = {}, plagiarism = {}%\n\n".format(lcs_length, plagiarism)
        ind += 1
    text_plagiarism = report_data['text_plagiarism'] * 100
    report += "Text average plagiarism (words): {}%".format(text_plagiarism)
    return report


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
