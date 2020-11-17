"""
Longest common subsequence problem
"""
import pickle
import os
import re
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
    tokens = []
    sentences = text.split('\n')
    for sentence in sentences:
        token_sentence = tuple(tokenize(sentence))
        if token_sentence:
            tokens.append(token_sentence)
    return tuple(tokens)


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not isinstance(rows, int) or not isinstance(columns, int) or \
            isinstance(rows, bool) or isinstance(columns, bool):
        return []
    zero_matrix = []
    n_columns = [0] * columns
    if n_columns:
        zero_matrix = [[0] * columns for _ in range(rows)]
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or \
            None in first_sentence_tokens or None in second_sentence_tokens:
        return []
    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for row, word_1 in enumerate(first_sentence_tokens):
        for column, word_2 in enumerate(second_sentence_tokens):
            if word_1 == word_2:
                lcs_matrix[row][column] = lcs_matrix[row - 1][column - 1] + 1
            else:
                lcs_matrix[row][column] = max((lcs_matrix[row][column - 1], lcs_matrix[row - 1][column]))
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
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or \
            not isinstance(plagiarism_threshold, float):
        return -1
    if None in first_sentence_tokens or None in second_sentence_tokens or \
            plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1
    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return 0
    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if len(first_sentence_tokens) > len(second_sentence_tokens):
        lcs_length = max(lcs_matrix[len(second_sentence_tokens)-1])
    else:
        lcs_length = max(lcs_matrix[-1])
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
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or \
            None in first_sentence_tokens or None in second_sentence_tokens:
        return ()
    if not isinstance(lcs_matrix, list) or None in lcs_matrix or \
            (isinstance(lcs_matrix, list) and None in lcs_matrix):
        return ()
    if isinstance(lcs_matrix, list) and len(lcs_matrix) > 0:
        if isinstance(lcs_matrix[0], list) and None in lcs_matrix[0]:
            return ()
    lcs = []
    if lcs_matrix:
        if len(lcs_matrix) == len(first_sentence_tokens) and \
                len(lcs_matrix[0]) == len(second_sentence_tokens):
            if lcs_matrix[0][0] > 1:
                return ()
            rows = len(first_sentence_tokens) - 1
            columns = len(second_sentence_tokens) - 1
            while rows > 0 and columns > 0:
                if first_sentence_tokens[rows] == second_sentence_tokens[columns]:
                    lcs.append(first_sentence_tokens[rows])
                    rows -= 1
                    columns -= 1
                elif lcs_matrix[rows - 1][columns] > lcs_matrix[rows][columns - 1]:
                    rows -= 1
                else:
                    columns -= 1
            if lcs_matrix[0][0] != 0:
                lcs.append(first_sentence_tokens[0])
    return tuple(lcs[::-1])


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
            None in original_text_tokens or None in suspicious_text_tokens or\
            not isinstance(plagiarism_threshold, float):
        return -1
    if not 0 < plagiarism_threshold < 1:
        return -1
    if isinstance(original_text_tokens, tuple) and len(original_text_tokens) > 0:
        if isinstance(original_text_tokens[0], tuple) and\
                (None in original_text_tokens[0] or '' in original_text_tokens[0]):
            return -1
    if isinstance(suspicious_text_tokens, tuple) and len(suspicious_text_tokens) > 0:
        if isinstance(suspicious_text_tokens[0], tuple) and\
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
    if not isinstance(original_sentence_tokens, tuple) or not isinstance(suspicious_sentence_tokens, tuple) or \
            not isinstance(lcs, tuple):
        return ()
    if None in original_sentence_tokens or None in suspicious_sentence_tokens or None in lcs:
        return ()
    diff_indexes = []
    changed_words_indexes = [index for index, token in enumerate(suspicious_sentence_tokens) if token not in lcs]
    for number, index in enumerate(changed_words_indexes):
        if len(changed_words_indexes)-1 != number:
            if index + 1 != changed_words_indexes[number + 1] and index - 1 not in diff_indexes:
                diff_indexes.extend([index, index + 1])
            elif index - 1 not in changed_words_indexes and index + 1 in changed_words_indexes:
                diff_indexes.append(index)
            elif index - 1 in changed_words_indexes and index + 1 not in changed_words_indexes:
                diff_indexes.append(index+1)
        elif len(changed_words_indexes)-1 == number:
            if index - 1 != changed_words_indexes[number - 1]:
                diff_indexes.extend([index, index + 1])
            elif index - 1 == changed_words_indexes[number - 1]:
                diff_indexes.append(index + 1)
    if original_sentence_tokens == ():
        return tuple([(), tuple(diff_indexes)])
    return tuple([tuple(diff_indexes), tuple(diff_indexes)])


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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) or \
            not isinstance(accumulated_diff_stats, dict):
        return ''
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += tuple([tuple([''])]) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]
    report = []
    total_plagiarism_percent = accumulated_diff_stats['text_plagiarism'] * 100
    for number in enumerate(suspicious_text_tokens):
        number = number[0]
        lcs_length = accumulated_diff_stats['sentence_lcs_length'][number]
        plagiarism_percent = accumulated_diff_stats['sentence_plagiarism'][number] * 100
        diff_indexes = accumulated_diff_stats['difference_indexes'][number]
        changed_original = list(original_text_tokens[number])
        changed_suspicious = list(suspicious_text_tokens[number])
        if diff_indexes != ((), ()):
            for element, indexes in enumerate(diff_indexes):
                inserts = 0
                for insert in indexes:
                    if element == 0:
                        changed_suspicious.insert(insert + inserts, '|')
                    elif element == 1:
                        changed_original.insert(insert + inserts, '|')
                    inserts += 1
        report.append('- ' + ' '.join(changed_original))
        report.append('+ ' + ' '.join(changed_suspicious))
        report.append('lcs = {}, plagiarism = {}%'.format(lcs_length, plagiarism_percent))
    report.append('Text average plagiarism (words): {}%'.format(total_plagiarism_percent))
    return ' '.join(report)


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
    len_search = min(len(first_sentence_tokens), len(second_sentence_tokens))
    cur_row = [0] * (len_search + 1)
    for w_1 in first_sentence_tokens:
        prev_row = cur_row[:]
        for col, w_2 in enumerate(second_sentence_tokens):
            if w_1 == w_2:
                cur_row[col + 1] = prev_row[col] + 1
            else:
                cur_row[col + 1] = max((cur_row[col], prev_row[col + 1]))
    lcs_len = cur_row[-1]
    if lcs_len / len(second_sentence_tokens) < plagiarism_threshold:
        return 0
    return lcs_len if not lcs_len / len(second_sentence_tokens) < plagiarism_threshold else 0


def tokenize_big_file(path_to_file: str, ids=0) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :param ids: an id
    :return: a tuple with ids
    """
    tokens = []
    if os.path.exists('id.pkl'):
        with open('id.pkl', 'rb') as put:
            id_dict = pickle.load(put)
    else:
        id_dict = {}
    with open(path_to_file, encoding='UTF-8') as file:
        for line in file:
            token_sentence = re.sub('[^a-z \n]', '', line.lower()).split()
            for token in token_sentence:
                if token not in id_dict:
                    id_dict[token] = ids
                    tokens.append(ids)
                    ids += 1
                else:
                    tokens.append(id_dict[token])
    with open('id.pkl', 'wb') as out:
        pickle.dump(id_dict, out)
    return tuple(tokens)
