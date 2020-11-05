"""
Longest common subsequence problem
"""
<<<<<<< HEAD
import tokenizer
=======
import pickle
import os
import re
from lab_2.tokenizer import tokenize
>>>>>>> upstream/master


def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
<<<<<<< HEAD

    if not isinstance(text, str):
        return ()

    tokens = []
    sentences = text.split('\n')
    for elems in sentences:
        tokenized_text = tuple(tokenizer.tokenize(elems))
        if tokenized_text:
            tokens.append(tokenized_text)
=======
    tokens = []
    sentences = text.split('\n')
    for sentence in sentences:
        token_sentence = tuple(tokenize(sentence))
        if token_sentence:
            tokens.append(token_sentence)
>>>>>>> upstream/master
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
<<<<<<< HEAD
    is_rows = not isinstance(rows, int) or isinstance(rows, bool)
    is_cols = not isinstance(columns, int) or isinstance(columns, bool)

    if is_rows or is_cols or rows <= 0 or columns <= 0:
        return []

    zero_matrix = []
    for _ in range(rows):
        zero_matrix.append([0] * columns)
=======
    if not isinstance(rows, int) or not isinstance(columns, int) or \
            isinstance(rows, bool) or isinstance(columns, bool):
        return []
    zero_matrix = []
    n_columns = [0] * columns
    if n_columns:
        zero_matrix = [[0] * columns for _ in range(rows)]
>>>>>>> upstream/master
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
<<<<<<< HEAD
    if (not isinstance(first_sentence_tokens, tuple)
            or not isinstance(second_sentence_tokens, tuple)
            or not all(isinstance(i, str) for i in first_sentence_tokens)
            or not all(isinstance(i, str) for i in second_sentence_tokens)):
        return []

    mtx = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    for idx1, elem1 in enumerate(first_sentence_tokens):
        for idx2, elem2 in enumerate(second_sentence_tokens):
            if elem1 == elem2:
                mtx[idx1][idx2] = mtx[idx1 - 1][idx2 - 1] + 1
            else:
                mtx[idx1][idx2] = max(mtx[idx1][idx2 - 1], mtx[idx1 - 1][idx2])
    return mtx
=======
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
>>>>>>> upstream/master


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
<<<<<<< HEAD
    sent1_check = not ((isinstance(first_sentence_tokens, tuple) and first_sentence_tokens
                     and first_sentence_tokens[0] is not None)
                     or (isinstance(first_sentence_tokens, tuple) and not first_sentence_tokens))
    sent2_check = not ((isinstance(second_sentence_tokens, tuple) and second_sentence_tokens
                     and second_sentence_tokens[0] is not None)
                     or (isinstance(second_sentence_tokens, tuple) and not second_sentence_tokens))
    threshold_check = (isinstance(plagiarism_threshold, (float, int))
                       and not isinstance(plagiarism_threshold, bool) and 0 < plagiarism_threshold < 1)

    if sent1_check or sent2_check or not threshold_check:
        return -1

    if len(first_sentence_tokens) > len(second_sentence_tokens):
        first_sentence_tokens = tuple(first_sentence_tokens[:len(second_sentence_tokens)])

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if not lcs_matrix:
        return 0

    lcs_len = lcs_matrix[-1][-1]
    sec_sent_len = len(second_sentence_tokens)
    divide = lcs_len / sec_sent_len

    if divide < plagiarism_threshold:
        return 0

    return lcs_len
=======
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
>>>>>>> upstream/master


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
<<<<<<< HEAD

    sent1_check = (not isinstance(first_sentence_tokens, tuple) or not first_sentence_tokens
                 or len(first_sentence_tokens) == 0 or first_sentence_tokens[0] is None
                 or not all(isinstance(word, str) for word in first_sentence_tokens))
    sent2_check = (not isinstance(second_sentence_tokens, tuple) or not second_sentence_tokens
                 or len(second_sentence_tokens) == 0 or second_sentence_tokens[0] is None
                 or not all(isinstance(word, str) for word in second_sentence_tokens))

    if sent1_check or sent2_check:
        return ()

    matrix_check = (not lcs_matrix or not isinstance(lcs_matrix, list)
                    or not all(isinstance(i, list) for i in lcs_matrix)
                    or not all(isinstance(i, int) for lists in lcs_matrix for i in lists)
                    or not lcs_matrix[0][0] in (0, 1)
                    or not len(lcs_matrix) == len(first_sentence_tokens)
                    or not len(lcs_matrix[0]) == len(second_sentence_tokens))

    if matrix_check:
        return ()

    lcs = []
    index_row, index_col = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1
    while index_row >= 0 and index_col >= 0:
        if first_sentence_tokens[index_row] == second_sentence_tokens[index_col]:
            lcs.append(first_sentence_tokens[index_row])
            index_row, index_col = index_row - 1, index_col - 1
        elif lcs_matrix[index_row - 1][index_col] > lcs_matrix[index_row][index_col - 1]:
            index_row -= 1
        else:
            if index_row == 1 or index_col == 0:
                index_row -= 1
            else:
                index_col -= 1

    lcs.reverse()
    return tuple(lcs)
=======
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
>>>>>>> upstream/master


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
<<<<<<< HEAD
    len_check = not isinstance(lcs_length, int) or isinstance(lcs_length, bool)

    susp_check = (not isinstance(suspicious_sentence_tokens, tuple)
                  or not all(isinstance(i, str) for i in suspicious_sentence_tokens))

    if isinstance(suspicious_sentence_tokens, tuple) and not suspicious_sentence_tokens:
        return 0

    if len_check or susp_check or not 0 <= lcs_length <= len(suspicious_sentence_tokens):
        return -1
=======
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
>>>>>>> upstream/master

    return lcs_length / len(suspicious_sentence_tokens)

<<<<<<< HEAD

=======
>>>>>>> upstream/master
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
<<<<<<< HEAD
    orig = original_text_tokens
    susp = suspicious_text_tokens

    orig_check = (not isinstance(orig, tuple)
                  or not all(isinstance(i, tuple) for i in orig)
                  or not all(isinstance(i, str) for subtuple in orig for i in subtuple))

    susp_check = (not isinstance(susp, tuple)
                  or not all(isinstance(i, tuple) for i in susp)
                  or not all(isinstance(i, str) for subtuple in susp for i in subtuple))

    plag_check = not isinstance(plagiarism_threshold, float) or plagiarism_threshold < 0 or plagiarism_threshold > 1

    if (isinstance(orig, tuple) and not any(orig) or
            isinstance(susp, tuple) and not any(susp)):
        return 0

    if orig_check or susp_check or plag_check:
        return -1

    if len(orig) < len(susp):
        orig = list(original_text_tokens)
        for i in range(len(susp) - len(orig)):
            orig.append(())
        orig = tuple(orig)

    p_scores = 0

    for i, susp_sentence in enumerate(susp):
        lcs_len = find_lcs_length(orig[i], susp_sentence, plagiarism_threshold)
        p_score = calculate_plagiarism_score(lcs_len, susp_sentence)
        p_scores += p_score

    return p_scores / len(susp)
=======
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
>>>>>>> upstream/master


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
<<<<<<< HEAD
    sentences_check = (not isinstance(original_sentence_tokens, tuple)
                       or not isinstance(suspicious_sentence_tokens, tuple)
                       or not all(isinstance(i, str) for i in original_sentence_tokens)
                       or not all(isinstance(i, str) for i in suspicious_sentence_tokens))

    lcs_check = (not isinstance(lcs, tuple)
                 or not all(isinstance(i, str) for i in lcs))

    if sentences_check or lcs_check:
        return ()

    difference_sum = []

    for sentence in (original_sentence_tokens, suspicious_sentence_tokens):

        difference = []
        for i, token in enumerate(sentence):

            if token not in lcs:
                if i == 0 or sentence[i - 1] in lcs:
                    difference.append(i)
                if i == len(sentence) - 1 or sentence[i + 1] in lcs:
                    difference.append(i + 1)

        difference_sum.append(tuple(difference))

    return tuple(difference_sum)
=======
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
>>>>>>> upstream/master


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
<<<<<<< HEAD
    orig = original_text_tokens
    susp = suspicious_text_tokens

    orig_check = not (isinstance(orig, tuple)
                      and all(isinstance(i, tuple) for i in orig)
                      and all(isinstance(i, str) for tokens in orig for i in tokens))
    susp_check = not (isinstance(susp, tuple)
                      and all(isinstance(i, tuple) for i in susp)
                      and all(isinstance(i, str) for tokens in susp for i in tokens))

    if orig_check or susp_check\
            or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return {}

    stats = {
        'text_plagiarism': calculate_text_plagiarism_score(orig, susp, plagiarism_threshold),
        'sentence_plagiarism': [],
        'sentence_lcs_length': [],
        'difference_indexes': []
    }

    if len(orig) < len(susp):
        orig = list(orig)
        for _ in range(len(susp) - len(orig)):
            orig.append(())
        orig = tuple(orig)

    for orig_sent, susp_sent in zip(orig, susp):
        lcs_len = find_lcs_length(orig_sent, susp_sent, plagiarism_threshold)
        stats['sentence_lcs_length'].append(lcs_len)
        stats['sentence_plagiarism'].append(calculate_plagiarism_score(lcs_len, susp_sent))
        lcs_matrix = fill_lcs_matrix(orig_sent, susp_sent)
        lcs = find_lcs(orig_sent, susp_sent, lcs_matrix)
        stats['difference_indexes'].append(find_diff_in_sentence(orig_sent, susp_sent, lcs))

    return stats
=======
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
>>>>>>> upstream/master


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
<<<<<<< HEAD
    orig = original_text_tokens
    susp = suspicious_text_tokens

    orig_check = not (isinstance(orig, tuple) and
                      all(isinstance(i, tuple) for i in orig) and
                      all(isinstance(i, str) for tokens in orig for i in tokens))
    susp_check = not (isinstance(susp, tuple) and
                      all(isinstance(i, tuple) for i in susp) and
                      all(isinstance(i, str) for tokens in susp for i in tokens))

    if not isinstance(accumulated_diff_stats, dict) or orig_check or susp_check:
        return ''

    if len(orig) < len(susp):
        orig += (()) * (len(susp) - len(orig))
    if len(orig) > len(susp):
        orig = orig[:len(susp)]

    report = ''

    for sent_idx, _ in enumerate(susp):
        if accumulated_diff_stats['difference_indexes'][sent_idx] == ((), ()):
            orig_sentence = ' '.join(orig[sent_idx])
            susp_sentence = ' '.join(susp[sent_idx])
        else:
            orig_sentence = list(orig[sent_idx])
            counter = 1
            for diff_idx in accumulated_diff_stats['difference_indexes'][sent_idx][0]:
                if counter % 2 != 0:
                    orig_sentence.insert(diff_idx, '|')
                    counter += 1
                else:
                    orig_sentence.insert(diff_idx + 1, '|')
                    counter += 1
            orig_sentence = ' '.join(orig_sentence)

            susp_sentence = list(susp[sent_idx])
            counter = 1
            for diff_idx in accumulated_diff_stats['difference_indexes'][sent_idx][1]:
                if counter % 2 != 0:
                    susp_sentence.insert(diff_idx, '|')
                    counter += 1
                else:
                    susp_sentence.insert(diff_idx + 1, '|')
                    counter += 1
            susp_sentence = ' '.join(susp_sentence)

        report += '- {}\n+ {}\n\nlcs = {}, plagiarism = {}%\n\n'.format(
            orig_sentence, susp_sentence, accumulated_diff_stats['sentence_lcs_length'][sent_idx],
            accumulated_diff_stats['sentence_plagiarism'][sent_idx] * 100)
    report += 'Text average plagiarism (words): {}%\n\n'.format(accumulated_diff_stats['text_plagiarism'] * 100)

    return report
=======
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
>>>>>>> upstream/master


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
<<<<<<< HEAD
    return 0
=======
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
>>>>>>> upstream/master


def tokenize_big_file(path_to_file: str, ids=0) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :param ids: an id
    :return: a tuple with ids
    """
<<<<<<< HEAD
    return ()
=======
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
>>>>>>> upstream/master
