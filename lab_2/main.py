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
    if not isinstance(text, str):
        return ()

    text = text.split('\n')

    text_tuple = ()
    for sentence in text:
        sentence_clear = tokenize(sentence)
        if not sentence_clear:
            continue
        text_tuple += (tuple(sentence_clear),)

    return text_tuple


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    is_rows_columns_correct = ((not isinstance(rows, bool)) and (not isinstance(columns, bool)) and
                               isinstance(rows, int) and isinstance(columns, int) and (rows > 0) and (columns > 0))
    if not is_rows_columns_correct:
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
    is_tuples_correct = isinstance(first_sentence_tokens, tuple) and isinstance(second_sentence_tokens, tuple)
    is_both_tuples_empty = not first_sentence_tokens or not second_sentence_tokens
    if not is_tuples_correct or is_both_tuples_empty:
        return []
    for word_1s in first_sentence_tokens:
        if not word_1s and not isinstance(word_1s, str):
            return []
    for word_2s in second_sentence_tokens:
        if not word_2s and not isinstance(word_2s, str):
            return []

    rows_first_sent = len(first_sentence_tokens)
    columns_second_sent = len(second_sentence_tokens)

    lcs_matrix = create_zero_matrix(rows_first_sent + 1, columns_second_sent + 1)

    for first_sent_word in range(1, rows_first_sent + 1):
        for second_sent_word in range(1, columns_second_sent + 1):
            if first_sentence_tokens[first_sent_word - 1] == second_sentence_tokens[second_sent_word - 1]:
                lcs_matrix[first_sent_word][second_sent_word] = lcs_matrix[first_sent_word - 1][second_sent_word - 1] \
                                                                + 1
            else:
                lcs_matrix[first_sent_word][second_sent_word] = max(lcs_matrix[first_sent_word - 1][second_sent_word],
                                                                    lcs_matrix[first_sent_word][second_sent_word - 1])

    del lcs_matrix[0]
    for row in lcs_matrix:
        del row[0]

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
    is_variables_incorrect = not (isinstance(first_sentence_tokens, tuple) and isinstance(second_sentence_tokens, tuple)
                                  and isinstance(plagiarism_threshold, float) and (0 <= plagiarism_threshold <= 1))

    if is_variables_incorrect:
        return -1
    for word_1s in first_sentence_tokens:
        if not isinstance(word_1s, str) or not word_1s:
            return -1
    for word_2s in second_sentence_tokens:
        if not isinstance(word_2s, str) or not word_2s:
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
    is_type_incorrect = not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
                        or not isinstance(lcs_matrix, list)
    is_tuples_matrix_empty = not first_sentence_tokens or not second_sentence_tokens or not lcs_matrix

    if is_type_incorrect or is_tuples_matrix_empty:
        return ()
    if (len(lcs_matrix) != len(first_sentence_tokens)) or (len(lcs_matrix[0]) != len(second_sentence_tokens)) or \
            (lcs_matrix[0][0] > 1):
        return ()

    lcs = []
    for index_r, row in enumerate(reversed(lcs_matrix)):
        for index_col, column in enumerate(reversed(row)):
            if not row or not column:
                return ()
            if first_sentence_tokens[index_r] == second_sentence_tokens[index_col]:
                lcs.append(second_sentence_tokens[index_col])

    lcs = tuple(lcs)

    return lcs


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    is_data_incorrect = not isinstance(suspicious_sentence_tokens, tuple) or not isinstance(lcs_length, int) or \
                        isinstance(lcs_length, bool) or not lcs_length >= 0
    if is_data_incorrect:
        return -1.0

    is_lengths_correspond = (not suspicious_sentence_tokens and lcs_length <= 0) or \
                            (suspicious_sentence_tokens and lcs_length > len(suspicious_sentence_tokens))
    if is_lengths_correspond:
        return -1.0

    for word in suspicious_sentence_tokens:
        if not isinstance(word, str) or not word:
            return -1.0

    if not suspicious_sentence_tokens:
        return 0.0
    plagiarism_score = lcs_length / len(suspicious_sentence_tokens)

    return plagiarism_score


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple,
                                    plagiarism_threshold) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    is_variables_incorrect = not (isinstance(original_text_tokens, tuple) and isinstance(suspicious_text_tokens, tuple)
                                  and isinstance(plagiarism_threshold, float) and (0 <= plagiarism_threshold <= 1))

    if is_variables_incorrect:
        return -1.0

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += ((),) * (len(suspicious_text_tokens) - len(original_text_tokens))
        original_text_length = len(original_text_tokens)
    else:
        original_text_length = len(original_text_tokens[:len(suspicious_text_tokens)])

    plagiarism_scores = ()
    for sentence_number in range(original_text_length):
        lcs_length = find_lcs_length(original_text_tokens[sentence_number], suspicious_text_tokens[sentence_number],
                                     plagiarism_threshold)
        if lcs_length == -1:
            return -1.0

        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[sentence_number])
        if plagiarism_score == -1:
            plagiarism_score = 0.0

        plagiarism_scores += (plagiarism_score,)

    plagiarism_result = sum(plagiarism_scores) / len(suspicious_text_tokens)

    return plagiarism_result


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    is_type_incorrect = not isinstance(original_sentence_tokens, tuple) or \
                        not isinstance(suspicious_sentence_tokens, tuple) or not isinstance(lcs, tuple)

    if is_type_incorrect or not all(original_sentence_tokens) or not all(suspicious_sentence_tokens) or not all(lcs):
        return ()

    indexes_diff_original = [original_sentence_tokens.index(word) for word in original_sentence_tokens
                             if word not in lcs]
    indexes_diff_suspicious = [suspicious_sentence_tokens.index(word) for word in suspicious_sentence_tokens
                               if word not in lcs]

    def find_diff_indexes(indexes_diff_words):
        changes_indexes = []
        for index, diff_word_index in enumerate(indexes_diff_words):
            changes_indexes.append(diff_word_index)
            if (index != 0) and (diff_word_index - indexes_diff_words[index - 1] == 1):
                del changes_indexes[changes_indexes.index(diff_word_index)]
            if (diff_word_index != indexes_diff_words[-1]) and indexes_diff_words[index + 1] - diff_word_index == 1:
                continue
            changes_indexes.append(diff_word_index + 1)

        return changes_indexes

    changes_indexes_both_sent = (tuple(find_diff_indexes(indexes_diff_original)),
                                 tuple(find_diff_indexes(indexes_diff_suspicious)))

    return changes_indexes_both_sent


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
    is_type_incorrect = not isinstance(original_text_tokens, tuple) or \
                        not isinstance(suspicious_text_tokens, tuple) or not isinstance(plagiarism_threshold, float) \
                        or not 0 <= plagiarism_threshold <= 1

    if is_type_incorrect or not all(original_text_tokens) or not all(suspicious_text_tokens):
        return {}

    text_plagiarism = calculate_text_plagiarism_score(original_text_tokens,
                                                      suspicious_text_tokens,
                                                      plagiarism_threshold)

    sentence_plagiarism = []
    sentence_lcs_length = []
    difference_indexes = []

    for index_sent in range(len(original_text_tokens)):
        lcs_matrix = fill_lcs_matrix(original_text_tokens[index_sent], suspicious_text_tokens[index_sent])
        lcs_length = find_lcs_length(original_text_tokens[index_sent],
                                     suspicious_text_tokens[index_sent],
                                     plagiarism_threshold)
        lcs = find_lcs(original_text_tokens[index_sent], suspicious_text_tokens[index_sent], lcs_matrix)
        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[index_sent])
        index_diff_in_sentence = find_diff_in_sentence(original_text_tokens[index_sent],
                                                       suspicious_text_tokens[index_sent],
                                                       lcs)
        sentence_plagiarism.append(plagiarism_score)
        sentence_lcs_length.append(lcs_length)
        difference_indexes.append(index_diff_in_sentence)

    diff_stats = {'text_plagiarism': text_plagiarism,
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
    is_type_incorrect = not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) \
                        or not isinstance(accumulated_diff_stats, dict)

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
