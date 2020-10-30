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
    tokens_tpl = []
    if isinstance(text, str) and text:
        text_full = text.split('\n')
        for token in text_full:
            if len(tokenizer.tokenize(token)):
                tokens = tuple(tokenizer.tokenize(token))
                tokens_tpl.append(tokens)
        return tuple(tokens_tpl)
    else:
        return ()


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    is_rows = not isinstance(rows, bool) and isinstance(rows, int) and rows > 0
    is_columns = not isinstance(columns, bool) and isinstance(columns, int) and columns > 0
    if not is_rows or not is_columns:
        return []

    matrix = [[0] * columns for _ in range(rows)]

    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if (not isinstance(first_sentence_tokens, tuple)
            or not isinstance(second_sentence_tokens, tuple)
            or not all(isinstance(i, str) for i in first_sentence_tokens)
            or not all(isinstance(i, str) for i in second_sentence_tokens)):
        return []

    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))  # r & c  по длинам
    for in_1, elem_1 in enumerate(first_sentence_tokens):
        for in_2, elem_2 in enumerate(second_sentence_tokens):
            if elem_1 == elem_2:
                lcs_matrix[in_1][in_2] = lcs_matrix[in_1 - 1][in_2 - 1] + 1
            else:
                lcs_matrix[in_1][in_2] = max(lcs_matrix[in_1][in_2 - 1], lcs_matrix[in_1 - 1][in_2])
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
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not isinstance(plagiarism_threshold, float) or None in first_sentence_tokens:
        return -1
    if None in second_sentence_tokens or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1

    if len(first_sentence_tokens) == 0 or not first_sentence_tokens \
            or len(second_sentence_tokens) == 0 or not second_sentence_tokens:
        return 0

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if len(first_sentence_tokens) > len(second_sentence_tokens):
        lcs_matrix = lcs_matrix[len(second_sentence_tokens) - 1][len(second_sentence_tokens) - 1]
    else:
        lcs_matrix = lcs_matrix[-1][-1]
    if lcs_matrix / len(second_sentence_tokens) < plagiarism_threshold:
        return 0
    return lcs_matrix


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not isinstance(lcs_matrix, list):
        return ()
    if not first_sentence_tokens \
            or not second_sentence_tokens or not lcs_matrix or None in lcs_matrix:
        return ()

    if lcs_matrix:
        if len(lcs_matrix) == len(first_sentence_tokens) and len(lcs_matrix[0]) == len(second_sentence_tokens):
            if lcs_matrix[0][0] > 1:
                return ()
    max_len = []
    for ind_1, el_1 in enumerate(reversed(lcs_matrix)):
        for ind_2, el_2 in enumerate(reversed(el_1)):
            if not el_1 or not el_2:
                return ()
            if first_sentence_tokens[ind_1] == second_sentence_tokens[ind_2]:
                max_len.append(second_sentence_tokens[ind_2])
    return tuple(max_len)


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int) and not isinstance(lcs_length, float) or isinstance(lcs_length, bool) or \
            not isinstance(suspicious_sentence_tokens, tuple) or None in suspicious_sentence_tokens:
        return -1
    if lcs_length > len(suspicious_sentence_tokens) > 0 or lcs_length < 0:
        return -1
    if not suspicious_sentence_tokens:
        plagiarism_score = 0.0
        return plagiarism_score
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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) or \
            None in original_text_tokens or None in suspicious_text_tokens or \
            not isinstance(plagiarism_threshold, float):
        return -1
    if not 0 < plagiarism_threshold < 1:
        return -1
    if isinstance(original_text_tokens, tuple) and len(original_text_tokens) > 0:
        if isinstance(original_text_tokens[0], tuple) and \
                (None in original_text_tokens[0] or '' in original_text_tokens[0]):
            return -1
    if isinstance(suspicious_text_tokens, tuple) and len(suspicious_text_tokens) > 0:
        if isinstance(suspicious_text_tokens[0], tuple) and \
                (None in suspicious_text_tokens[0] or '' in suspicious_text_tokens[0]):
            return -1
    plagiarism_scores = []
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += tuple([tuple([''])]) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]
    for original_number, original_sentence in enumerate(original_text_tokens):
        for suspicious_number, suspicious_sentence in enumerate(suspicious_text_tokens):
            if original_number == suspicious_number:
                lcs_length = int(find_lcs_length(original_sentence, suspicious_sentence, plagiarism_threshold))
                plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_sentence)
                plagiarism_scores.append(plagiarism_score)
    total_plagiarism_score = sum(plagiarism_scores) / len(suspicious_text_tokens)
    return total_plagiarism_score


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
    diff_stats = {'sentence_plagiarism': [], 'sentence_lcs_length': [], 'difference_indexes': []}
    for original_number, original_sentence in enumerate(original_text_tokens):
        for suspicious_number, suspicious_sentence in enumerate(suspicious_text_tokens):
            if original_number == suspicious_number:
                lcs_length = int(find_lcs_length(original_sentence, suspicious_sentence, plagiarism_threshold))
                lcs_matrix = fill_lcs_matrix(original_sentence, suspicious_sentence)
                lcs = find_lcs(original_sentence, suspicious_sentence, lcs_matrix)
                diff_stats['sentence_lcs_length'] += [lcs_length]
                diff_stats['difference_indexes'] += [find_diff_in_sentence(original_sentence, suspicious_sentence, lcs)]
                plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_sentence)
                if plagiarism_score == -1:
                    diff_stats['sentence_plagiarism'] += [0.0]
                else:
                    diff_stats['sentence_plagiarism'] += [plagiarism_score]
        diff_stats['text_plagiarism'] = sum(diff_stats['sentence_plagiarism']) / len(suspicious_text_tokens)
    return diff_stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    is_type_incorrect = (not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple)
                         or not isinstance(accumulated_diff_stats, dict))

    if is_type_incorrect:
        return ''

    texts_length = len(original_text_tokens)

    report = ''


    for index_sent in range(texts_length):
        original_sentence = list(original_text_tokens[index_sent])
        suspicious_sentence = list(suspicious_text_tokens[index_sent])
        difference_indexes = accumulated_diff_stats['difference_indexes'][index_sent]

        insert_number = 0
        for index in difference_indexes[0]:
            original_sentence.insert(index + insert_number, '|')
            suspicious_sentence.insert(index + insert_number, '|')
            insert_number += 1

        original_sentence = ' '.join(original_sentence)
        suspicious_sentence = ' '.join(suspicious_sentence)

        lcs = accumulated_diff_stats['sentence_lcs_length'][index_sent]
        sentence_plagiarism = float(accumulated_diff_stats['sentence_plagiarism'][index_sent] * 100)
        report += '- {}\n+ {}\n\nlcs = {}, plagiarism = {}%\n\n'.format(original_sentence,
                                                                suspicious_sentence,
                                                                lcs,
                                                                sentence_plagiarism)

    text_plagiarism = float(accumulated_diff_stats['text_plagiarism'] * 100)
    report += 'Text average plagiarism (words): {}%'.format(text_plagiarism)

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
