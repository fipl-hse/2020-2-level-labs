"""
Longest common subsequence problem
"""
# import re
import csv
from copy import deepcopy
from tokenizer import tokenize


def are_inputs_incorrect(first_sentence_tokens, second_sentence_tokens, plagiarism_threshold=-100):
    first_is_not_tuple = not isinstance(first_sentence_tokens, tuple)
    second_is_not_tuple = not isinstance(second_sentence_tokens, tuple)
    threshold_is_not_float = not isinstance(plagiarism_threshold, float)

    if first_is_not_tuple or second_is_not_tuple:
        return True

    any_not_words_in_first = any(not isinstance(word, str) for word in first_sentence_tokens)
    any_not_words_in_second = any(not isinstance(word, str) for word in second_sentence_tokens)
    if any_not_words_in_first or any_not_words_in_second:
        return True

    if plagiarism_threshold != -100:
        if threshold_is_not_float or not 0 < plagiarism_threshold < 1:
            return True

    return False


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
    sentences = text.strip().split('\n')
    tokenized_sent = tuple(tuple(tokenize(sentence)) for sentence in sentences if len(sentence))
    return tokenized_sent


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    bad_rows_columns = (not isinstance(rows, int)
                        or not isinstance(columns, int)
                        or isinstance(rows, bool)
                        or isinstance(columns, bool))
    if bad_rows_columns:
        return []
    if (rows < 0) or (columns <= 0):
        return []
    zero_matrix = [[0] * columns for _ in range(rows)]
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    incorrect_inputs = are_inputs_incorrect(first_sentence_tokens, second_sentence_tokens)
    if incorrect_inputs or not first_sentence_tokens or not second_sentence_tokens:
        return []

    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for first_i, first_elem in enumerate(first_sentence_tokens):
        for sec_i, second_elem in enumerate(second_sentence_tokens):
            if first_elem == second_elem:
                lcs_matrix[first_i][sec_i] = lcs_matrix[first_i - 1][sec_i - 1] + 1
            else:
                lcs_matrix[first_i][sec_i] = max(lcs_matrix[first_i][sec_i - 1], lcs_matrix[first_i - 1][sec_i])

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
    incorrect_inputs = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)
                        or not isinstance(plagiarism_threshold, float))
    if incorrect_inputs:
        return -1
    bad_inputs = None in first_sentence_tokens or None in second_sentence_tokens or not 0 < plagiarism_threshold < 1
    if bad_inputs:
        return -1
    if len(first_sentence_tokens) > len(second_sentence_tokens):
        first_sentence_tokens = first_sentence_tokens[:len(second_sentence_tokens)]
    else:
        second_sentence_tokens = second_sentence_tokens[:len(first_sentence_tokens)]

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if lcs_matrix:
        length_lcs = lcs_matrix[-1][-1]
    else:
        return 0

    if (length_lcs / len(second_sentence_tokens)) < plagiarism_threshold:
        return 0

    return length_lcs


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    incorrect_inputs = are_inputs_incorrect(first_sentence_tokens, second_sentence_tokens)
    bad_arguments = (not isinstance(lcs_matrix, list) or not first_sentence_tokens or not second_sentence_tokens)
    if incorrect_inputs or bad_arguments:
        return ()

    incorrect_elements = (not all(isinstance(row, list) for row in lcs_matrix) or not lcs_matrix
                          or not all(isinstance(num, int) for num in lcs_matrix[0]))
    if incorrect_elements:
        return ()
    bad_input_matrix = (all(lcs_matrix[ind][:] for ind in range(len(lcs_matrix))) == 0
                        or len(lcs_matrix) != len(first_sentence_tokens)
                        or len(lcs_matrix[0]) != len(second_sentence_tokens)
                        or lcs_matrix[0][0] > 1)
    if bad_input_matrix:
        return ()

    lcs_matrix_copy = deepcopy(lcs_matrix)
    lcs_matrix_copy.append([0] * (len(first_sentence_tokens)))
    for row in lcs_matrix_copy:
        row.append(0)

    lcs = tuple()
    first_i, second_i = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1
    while first_i >= 0 and second_i >= 0:
        if first_sentence_tokens[first_i] == second_sentence_tokens[second_i]:
            lcs += (first_sentence_tokens[first_i], )
            first_i, second_i = first_i - 1, second_i - 1
        elif lcs_matrix_copy[first_i - 1][second_i] > lcs_matrix_copy[first_i][second_i - 1]:
            first_i -= 1
        else:
            second_i -= 1
    lcs = lcs[::-1]

    return lcs


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    input_not_tuple = not isinstance(suspicious_sentence_tokens, tuple)
    if not isinstance(lcs_length, int) or lcs_length < 0 or isinstance(lcs_length, bool) or input_not_tuple:
        return -1.0

    bad_inputs_tokens = (not all(isinstance(word, str) for word in suspicious_sentence_tokens)
                         or not all(len(word) for word in suspicious_sentence_tokens)
                         or lcs_length > len(suspicious_sentence_tokens)
                         or not suspicious_sentence_tokens)
    if not suspicious_sentence_tokens and lcs_length:
        return 0.0
    if bad_inputs_tokens:
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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return -1.0

    if len(original_text_tokens) < len(suspicious_text_tokens):
        n_lines_need = len(suspicious_text_tokens) - len(original_text_tokens)
        original_text_tokens += ((),) * n_lines_need
    else:
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]

    n_sentences = len(suspicious_text_tokens)

    for ind in range(n_sentences):
        first_sent = original_text_tokens[ind]
        second_sent = suspicious_text_tokens[ind]
        incorrect_input = are_inputs_incorrect(first_sent, second_sent, plagiarism_threshold)
        if incorrect_input:
            return -1.0
        bad_inputs_tokens = (not all(len(word) for word in first_sent)
                             or not all(len(word) for word in second_sent))
        if bad_inputs_tokens:
            return -1.0

    plagiarism_for_lines = []
    for n_line in range(n_sentences):
        lcs_length = find_lcs_length(original_text_tokens[n_line], suspicious_text_tokens[n_line], plagiarism_threshold)
        line_plagiarism = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[n_line])
        if line_plagiarism == -1:
            line_plagiarism = 0.0
        plagiarism_for_lines.append(line_plagiarism)

    plagiarism_result = sum(plagiarism_for_lines) / len(plagiarism_for_lines)

    return plagiarism_result


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    def find_diff(sentence):
        diff_words = tuple(sentence.index(word) for word in sentence if word not in lcs)
        indexes_diff_parts = tuple()
        for ind, word_index in enumerate(diff_words):
            if word_index - diff_words[ind - 1] != 1:
                indexes_diff_parts += (word_index, )
            if word_index != diff_words[-1] and (diff_words[ind + 1] - word_index == 1):
                continue
            indexes_diff_parts += (word_index + 1, )

        return indexes_diff_parts

    incorrect_input = are_inputs_incorrect(original_sentence_tokens, suspicious_sentence_tokens)
    if incorrect_input or not isinstance(lcs, tuple):
        return ()
    no_words_in_lcs = any(not isinstance(word, str) for word in lcs)
    if no_words_in_lcs:
        return ()

    diff_parts_both_sent = (find_diff(original_sentence_tokens), find_diff(suspicious_sentence_tokens))

    return diff_parts_both_sent


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
    incorrect_input = (not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple)
                       or not isinstance(plagiarism_threshold, float) or not 0 <= plagiarism_threshold <= 1)
    if incorrect_input:
        return {}
    if not all(original_text_tokens) or not all(suspicious_text_tokens):
        return {}

    sentence_plagiarism = []
    sentence_lcs_length = []
    difference_indexes = []

    n_sentences = len(suspicious_text_tokens)

    for sent_ind in range(n_sentences):
        lcs_matrix = fill_lcs_matrix(original_text_tokens[sent_ind], suspicious_text_tokens[sent_ind])
        lcs_length = find_lcs_length(original_text_tokens[sent_ind], suspicious_text_tokens[sent_ind],
                                     plagiarism_threshold)
        lcs = find_lcs(original_text_tokens[sent_ind], suspicious_text_tokens[sent_ind],
                       lcs_matrix)
        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[sent_ind])
        diff_in_sentence = find_diff_in_sentence(original_text_tokens[sent_ind], suspicious_text_tokens[sent_ind], lcs)

        sentence_plagiarism.append(plagiarism_score)
        sentence_lcs_length.append(lcs_length)
        difference_indexes.append(diff_in_sentence)

    diff_stats = {'text_plagiarism': calculate_text_plagiarism_score(original_text_tokens,
                                                                     suspicious_text_tokens,
                                                                     plagiarism_threshold),
                  'sentence_plagiarism': sentence_plagiarism,
                  'sentence_lcs_length': sentence_lcs_length,
                  'difference_indexes': difference_indexes}

    return diff_stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    incorrect_input = (not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple))

    if incorrect_input or not isinstance(accumulated_diff_stats, dict):
        return ''

    result_stat = ''
    n_sentences = len(suspicious_text_tokens)

    for sent_ind in range(n_sentences):
        orig_sentence = list(original_text_tokens[sent_ind])
        susp_sentence = list(suspicious_text_tokens[sent_ind])
        difference_indexes = accumulated_diff_stats['difference_indexes'][sent_ind]

        change_ind = 0
        for index in difference_indexes[0]:
            orig_sentence.insert(index + change_ind, '|')
            susp_sentence.insert(index + change_ind, '|')
            change_ind += 1

        orig_sentence = ' '.join(orig_sentence)
        susp_sentence = ' '.join(susp_sentence)

        sent_lcs_length = accumulated_diff_stats['sentence_lcs_length'][sent_ind]
        sent_plag = float(accumulated_diff_stats['sentence_plagiarism'][sent_ind] * 100)

        result_stat += f"- {orig_sentence}\n+ {susp_sentence}\n\nlcs = {sent_lcs_length}, plagiarism = {sent_plag}%\n\n"

    text_plagiarism = accumulated_diff_stats['text_plagiarism'] * 100

    result_stat += f"Text average plagiarism (words): {text_plagiarism}%"

    return result_stat


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
    # incorrect_inputs = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)
    #                     or not isinstance(plagiarism_threshold, float))
    # if incorrect_inputs:
    #     return -1

    if len(first_sentence_tokens) < len(second_sentence_tokens):
        len_need = len(first_sentence_tokens)
    else:
        len_need = len(second_sentence_tokens)

    current = [0] * (len_need + 1)
    for word_first in first_sentence_tokens[:len_need]:
        previous = current[:]
        for ind_second, word_second in enumerate(second_sentence_tokens[:len_need]):
            if word_first == word_second:
                current[ind_second + 1] = previous[ind_second] + 1
            else:
                current[ind_second + 1] = max(current[ind_second], previous[ind_second + 1])
    length_lcs = current[-1]

    if (length_lcs / len(second_sentence_tokens)) < plagiarism_threshold:
        return 0

    return length_lcs


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    with open('numeric_words.csv', 'r', encoding="utf-8") as file_with_words:
        reader = csv.reader(file_with_words)
        words_dict = {row[0]: int(row[1]) for row in reader}

    numeric_tokens = []
    with open(path_to_file, encoding='utf-8') as big_file:
        for line in big_file:
            line_tokens = tokenize(line)
            numeric_tokens.extend([words_dict[token] for token in line_tokens])

    return tuple(numeric_tokens)

