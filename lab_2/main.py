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
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))"""
    tuple_of_tokens = ()

    if not isinstance(text, str):
        return tuple_of_tokens

    lines = text.split('\n')
    tokens = []
    for line in lines:
        line_tuple = tuple(tokenizer.tokenize(line))
        if line_tuple:
            tokens.append(line_tuple)
    tuple_of_tokens = tuple(tokens)

    return tuple_of_tokens



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
    num_columns = [0] * columns
    if num_columns:
        zero_matrix = [[0] * columns for _ in range(rows)]
    return zero_matrix



def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """

    checking_first_sentence = (not isinstance(first_sentence_tokens, tuple) or
                                   None in first_sentence_tokens)
    checking_second_sentence = (not isinstance(second_sentence_tokens, tuple) or
                                    None in second_sentence_tokens)
    if checking_first_sentence or checking_second_sentence:
        return[]
    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for row, first_word in enumerate(first_sentence_tokens):
        for column, second_word in enumerate(second_sentence_tokens):
            if first_word == second_word:
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

    checking_first_sentence = (not isinstance(first_sentence_tokens, tuple) or
                               None in first_sentence_tokens)
    checking_second_sentence = (not isinstance(second_sentence_tokens, tuple) or
                                None in second_sentence_tokens)
    checking_plagiarism_threshold = (not isinstance(plagiarism_threshold, float) or
                                         plagiarism_threshold < 0 or
                                         plagiarism_threshold > 1)
    if checking_first_sentence or checking_second_sentence or checking_plagiarism_threshold:
        return -1
    if not first_sentence_tokens or not second_sentence_tokens:
        return 0
    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return 0
    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if len(first_sentence_tokens) > len(second_sentence_tokens):
        lcs_length = max(lcs_matrix[len(second_sentence_tokens) - 1])
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

    checking_first_sentence = (not isinstance(first_sentence_tokens, tuple) or
                               None in first_sentence_tokens)
    checking_second_sentence = (not isinstance(second_sentence_tokens, tuple) or
                                None in second_sentence_tokens)
    checking_lcs_matrix = (not lcs_matrix or
                               not isinstance(lcs_matrix, list))
    if checking_lcs_matrix or checking_first_sentence or checking_second_sentence:
        return ()
    length_1 = len(first_sentence_tokens)
    length_2 = len(second_sentence_tokens)
    if len(lcs_matrix) != length_1 or len(lcs_matrix[0]) != length_2:
        return ()
    if lcs_matrix[0][0] != 0 and lcs_matrix[0][0] != 1:
        return ()
    lcs_list = []
    row = len(first_sentence_tokens) - 1
    column = len(second_sentence_tokens) - 1
    if row < 0:
        row = 0
    elif column < 0:
        column = 0
    while row >= 0 and column >= 0:
        if first_sentence_tokens[row] == second_sentence_tokens[column]:
            lcs_list.append(second_sentence_tokens[column])
            row -= 1
            column -= 1
        else:
            if lcs_matrix[row - 1][column] > lcs_matrix[row][column - 1] or column == 0:
                row -= 1
            else:
                column -= 1
    return tuple(reversed(lcs_list))



def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """

    checking_lcs_length = (not isinstance(lcs_length, int) or
                               isinstance(lcs_length, bool) or
                               lcs_length < 0)
    checking_sentence = (not isinstance(suspicious_sentence_tokens, tuple) or
                             None in suspicious_sentence_tokens)

    if checking_lcs_length or checking_sentence:
        return -1.0
    if (len(suspicious_sentence_tokens) > 0 and lcs_length > len(suspicious_sentence_tokens) or
            lcs_length == 0 and len(suspicious_sentence_tokens) == 0):
        return -1.0

    plagiarism_score = lcs_length / len(suspicious_sentence_tokens) if (suspicious_sentence_tokens) else 0.0
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
    checking_plagiarism_threshold = (not isinstance(plagiarism_threshold, float) or
                                         plagiarism_threshold < 0 or
                                         plagiarism_threshold > 1)
    checking_original_text = (not isinstance(original_text_tokens, tuple) or
                                  None in original_text_tokens[0] or
                                  '' in original_text_tokens[0])
    checking_suspicious_text = (not isinstance(suspicious_text_tokens, tuple) or
                                    None in suspicious_text_tokens[0] or
                                    '' in suspicious_text_tokens[0])

    if checking_plagiarism_threshold or checking_original_text or checking_suspicious_text:
        return -1.0

    if len(original_text_tokens) < len(suspicious_text_tokens):
        while len(original_text_tokens) != len(suspicious_text_tokens):
            original_text_tokens += ('',)

    plagiarism_scores = []

    for idx, sentence_in_text_2 in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[idx], sentence_in_text_2, plagiarism_threshold)
        plagiarism = calculate_plagiarism_score(lcs_length, sentence_in_text_2)

        if original_text_tokens[idx] == sentence_in_text_2:
            plagiarism_scores.append(1)
        elif plagiarism != -1:
            plagiarism_scores.append(plagiarism)
        else:
            plagiarism_scores.append(0.0)

    text_plagiarism_score = sum(plagiarism_scores) / len(suspicious_text_tokens)

    return text_plagiarism_score


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
        if len(changed_words_indexes) - 1 != number:
            if index + 1 != changed_words_indexes[number + 1] and index - 1 not in diff_indexes:
                diff_indexes.extend([index, index + 1])
            elif index - 1 not in changed_words_indexes and index + 1 in changed_words_indexes:
                diff_indexes.append(index)
            elif index - 1 in changed_words_indexes and index + 1 not in changed_words_indexes:
                diff_indexes.append(index + 1)
        elif len(changed_words_indexes) - 1 == number:
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
    original_check = not (isinstance(original_text_tokens, tuple)
                          and all(isinstance(i, tuple) for i in original_text_tokens)
                          and all(isinstance(i, str) for tokens in original_text_tokens for i in tokens))
    suspicious_check = not (isinstance(suspicious_text_tokens, tuple)
                            and all(isinstance(i, tuple) for i in suspicious_text_tokens)
                            and all(isinstance(i, str) for tokens in suspicious_text_tokens for i in tokens))

    if original_check or suspicious_check or not isinstance(accumulated_diff_stats, dict):
        return ''

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += (()) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]

    def sentence_with_lines(sentences, index):
        for i in range(0, len(index), 2):
            if index[i] + 1 == index[i + 1]:
                sentences[index[i]] = f'| {sentences[index[i]]} |'
            else:
                sentences[index[i]] = f'| {sentences[index[i]]}'
                sentences[index[i + 1] - 1] = f'{sentences[index[i + 1] - 1]} |'
        return ' '.join(sentences)

    report = ''

    for i, (original_i, suspicious_i) \
            in enumerate(accumulated_diff_stats['difference_indexes']):
        original = list(original_text_tokens[i])
        suspicious = list(suspicious_text_tokens[i])
        lcs_length = accumulated_diff_stats['sentence_lcs_length'][i]
        plagiarism = accumulated_diff_stats['sentence_plagiarism'][i] * 100
        report += f'- {sentence_with_lines(original, original_i)}\n'
        report += f'+ {sentence_with_lines(suspicious, suspicious_i)}\n'
        report += f"\nlcs = {lcs_length}, plagiarism = {plagiarism}%\n\n"

    report += f'Text average plagiarism (words): {accumulated_diff_stats["text_plagiarism"] * 100}%'
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
    lcs_length = 0
    return lcs_length


def tokenize_big_file(path_to_file: str, ids=0) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :param ids: an id
    :return: a tuple with ids
    """
    tokens_tuple = ()
    return tokens_tuple
