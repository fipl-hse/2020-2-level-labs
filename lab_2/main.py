"""
Longest common subsequence problem
"""

import pickle
import re

from decorators import input_checker
from tokenizer import tokenize


@input_checker
def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    text = text.split('\n')
    sent = (tokenize(sent) for sent in text)
    return tuple(tokens for tokens in sent if tokens)


@input_checker
def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if columns == 0:
        return []

    return [[0 for _ in range(columns)] for __ in range(rows)]


@input_checker
def fill_lcs_matrix(first_sentence_tokens: tuple,
                    second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    matrix = create_zero_matrix(len(first_sentence_tokens),
                                len(second_sentence_tokens))

    for i, word1 in enumerate(first_sentence_tokens):
        for j, word2 in enumerate(second_sentence_tokens):
            if word1 == word2:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1]) + 1
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])
    return matrix


@input_checker
def find_lcs_length(first_sentence_tokens: tuple,
                    second_sentence_tokens: tuple,
                    plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    matrix = fill_lcs_matrix(first_sentence_tokens,
                             second_sentence_tokens)
    if matrix:
        lcs_length = matrix[-1][-1]
        if lcs_length / len(second_sentence_tokens) > plagiarism_threshold:
            return lcs_length
    return 0


@input_checker
def find_lcs(first_sentence_tokens: tuple,
             second_sentence_tokens: tuple,
             lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if len(first_sentence_tokens) != len(lcs_matrix) or \
       len(second_sentence_tokens) != len(lcs_matrix[0]) or \
       lcs_matrix[0][0] not in (0, 1):
        return ()

    row = len(first_sentence_tokens) - 1
    column = len(second_sentence_tokens) - 1

    longest_lcs = []

    while row or column:
        if first_sentence_tokens[row] == second_sentence_tokens[column]:
            longest_lcs.append(first_sentence_tokens[row])
            row -= 1
            column -= 1
        elif lcs_matrix[row - 1][column] > lcs_matrix[row][column - 1] or not column:
            row -= 1
        else:
            column -= 1
    if first_sentence_tokens[0] == second_sentence_tokens[0]:
        longest_lcs.append(first_sentence_tokens[0])
    return tuple(longest_lcs[::-1])

@input_checker
def calculate_plagiarism_score(lcs_length: int,
                               suspicious_sentence_tokens: tuple
                               )-> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if lcs_length > len(suspicious_sentence_tokens) or \
       not all(isinstance(elem, str) for elem in suspicious_sentence_tokens):
        return -1
    return lcs_length / len(suspicious_sentence_tokens)

@input_checker
def calculate_text_plagiarism_score(original_text_tokens: tuple,
                                    suspicious_text_tokens: tuple,
                                    plagiarism_threshold: float=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    while len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += ('',)

    scores = []
    for susp_sent, orig_sent in zip(suspicious_text_tokens,
                                    original_text_tokens):
        lcs_length = find_lcs_length(orig_sent,
                                     susp_sent,
                                     plagiarism_threshold)
        score = calculate_plagiarism_score(lcs_length,
                                           susp_sent)
        if score >= 0:
            scores.append(score)

    text_score = sum(scores) / len(suspicious_text_tokens)

    return text_score


@input_checker
def find_diff(tokens: tuple,
              tokens_for_check: tuple,
              lcs: tuple) -> tuple:
    idx_lcs = 0
    indexes = []
    isnt_previous_match = False

    for idx, _ in enumerate(tokens):
        if idx_lcs == len(lcs):
            indexes.extend([idx, len(tokens)])
            break
        if tokens[idx] == lcs[idx_lcs]:
            idx_lcs += 1
            if isnt_previous_match:
                isnt_previous_match = False
                indexes.append(end)
        elif isnt_previous_match:
            end += 1
        else:
            isnt_previous_match = True
            start = idx
            end = idx + 1
            indexes.append(start)
    return tuple(indexes)


def find_diff_in_sentence(original_sentence_tokens: tuple,
                          suspicious_sentence_tokens: tuple,
                          lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    if isinstance(lcs, tuple) and not lcs:
        if not original_sentence_tokens:
            return ((), (0, len(suspicious_sentence_tokens)))
        return ((0, len(original_sentence_tokens)),
                (0, len(suspicious_sentence_tokens)))

    if original_sentence_tokens == suspicious_sentence_tokens\
    and original_sentence_tokens == lcs:
        return ((), ())

    if not (origin_indexes := find_diff(original_sentence_tokens,
                                        suspicious_sentence_tokens,
                                        lcs)):
        return origin_indexes
    if not (susp_indexes := find_diff(suspicious_sentence_tokens,
                                      original_sentence_tokens,
                                      lcs)):
        return susp_indexes

    return origin_indexes, susp_indexes


@input_checker
def accumulate_diff_stats(original_text_tokens: tuple,
                          suspicious_text_tokens: tuple,
                          plagiarism_threshold: float=0.3) -> dict:
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
    length = len(suspicious_text_tokens)
    while len(original_text_tokens) < length:
        original_text_tokens += ('',)

    stat =  {'text_plagiarism': 0,
            'sentence_plagiarism': [0] * length,
            'sentence_lcs_length': [0] * length,
            'difference_indexes': [0] * length}

    stat['text_plagiarism'] = calculate_text_plagiarism_score(
                                  original_text_tokens,
                                  suspicious_text_tokens,
                                  plagiarism_threshold)

    for i in range(length):
        lcs_length = find_lcs_length(original_text_tokens[i],
                                     suspicious_text_tokens[i],
                                     plagiarism_threshold=0.0)
        stat['sentence_plagiarism'][i] = calculate_plagiarism_score(
                                             lcs_length,
                                             suspicious_text_tokens[i])

        stat['sentence_lcs_length'][i] = lcs_length

        lcs_matrix = fill_lcs_matrix(original_text_tokens[i],
                                     suspicious_text_tokens[i])
        lcs = find_lcs(original_text_tokens[i],
                       suspicious_text_tokens[i],
                       lcs_matrix)
        stat['difference_indexes'][i] = find_diff_in_sentence(
                                            original_text_tokens[i],
                                            suspicious_text_tokens[i],
                                            lcs)
    return stat


def sentence_report(sentence: tuple, indexes:tuple) -> str:
    start = end = 0
    report = ''
    for i in indexes:
        end = i
        report += ' '.join(sentence[start:end] + ('| ',))
        start = i
    report += ' '.join(sentence[end:])
    return report


@input_checker
def create_diff_report(original_text_tokens: tuple,
                       suspicious_text_tokens: tuple,
                       accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    report = ''
    for idx, (orig_idx, susp_idx) in enumerate(
      accumulated_diff_stats['difference_indexes']):
        orig = sentence_report(original_text_tokens[idx], orig_idx)
        susp = sentence_report(suspicious_text_tokens[idx], susp_idx)
        lcs = accumulated_diff_stats['sentence_lcs_length'][idx]
        score = accumulated_diff_stats['sentence_plagiarism'][idx] * 100
        report += f'- {orig}\n+ {susp}\n\nlcs = {lcs}, plagiarism = {score}%\n\n'
    text_score = accumulated_diff_stats['text_plagiarism'] * 100
    report += f'Text average plagiarism (words): {text_score}%'
    return report


def find_lcs_length_optimized(first_sentence_tokens: tuple,
                              second_sentence_tokens: tuple,
                              plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Hirschberg's algorithm
    At the same time, if the first and last tokens coincide,
    they are immediately added to lcs and not analyzed
    :param first_sentence_tokens: a list of tokens
    :param second_sentence_tokens: a list of tokens
    :return: a length of the longest common subsequence
    """
    
    #if first_sentence_tokens == second_sentence_tokens:
    #    return len(first_sentence_tokens)

    length = max(len(first_sentence_tokens), len(second_sentence_tokens))
    x_vector = [0 for _ in range(len(second_sentence_tokens))]
    for x_word in first_sentence_tokens[:length]:
        if x_word not in second_sentence_tokens[:length]:
            continue
        for i, y_word in enumerate(second_sentence_tokens[:length]):
            if x_word == y_word:
                x_vector[i] += 1
            else:
                x_vector[i] = max(x_vector[i - 1], x_vector[i])
    
    lcs_length = x_vector[-1]
    if lcs_length / len(second_sentence_tokens) > plagiarism_threshold:
        return lcs_length
    return 0


with open('lab_2/vocabulary.pickle', 'rb') as file:
    vocabulary = pickle.load(file)


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    indexes = tuple()
    with open(path_to_file, 'r', encoding='utf-8') as file:
        for line in file:
            tokens = re.sub('[^a-z \n]', '', line.lower()).split()
            indexes += tuple(vocabulary[token] for token in tokens)
    return indexes
