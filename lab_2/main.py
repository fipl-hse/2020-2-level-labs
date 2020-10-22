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
    lines = []
    text = text.split('\n')
    for i in text:
        line = tuple(tokenize(i))
        if line:
            lines.append(line)
    return tuple(lines)




def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    check = (not isinstance(rows, int) or not isinstance(columns, int) or isinstance(rows, bool)
               or isinstance(columns, bool))
    if check or not rows > 0 or not columns > 0:
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

    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or None in first_sentence_tokens or None in second_sentence_tokens:
        return []
    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for index1, element1 in enumerate(first_sentence_tokens):
        for index2, element2 in enumerate(second_sentence_tokens):
            if element1 == element2:
                lcs_matrix[index1][index2] = lcs_matrix[index1 - 1][index2 - 1] + 1
            else:
                lcs_matrix[index1][index2] = max(lcs_matrix[index1][index2 - 1], lcs_matrix[index1 - 1][index2])
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
    check = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)
            or not isinstance(plagiarism_threshold, float) or None in first_sentence_tokens
            or None in second_sentence_tokens or plagiarism_threshold < 0 or plagiarism_threshold > 1)
    if check :
        return -1
    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
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
    check = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)
            or not first_sentence_tokens or not second_sentence_tokens or
            not all(isinstance(i, str) for i in first_sentence_tokens)
            or not all(isinstance(i, str) for i in second_sentence_tokens))
    if check:
        return ()
    check_1 = (not isinstance(lcs_matrix, list) or not lcs_matrix or not all(isinstance(i, list) for i in lcs_matrix)
            or not (lcs_matrix[0][0] == 0 or lcs_matrix[0][0] == 1)
            or not len(lcs_matrix) == len(first_sentence_tokens)
            or not len(lcs_matrix[0]) == len(second_sentence_tokens))
    if check_1:
        return ()
    lcs = []
    for index_1, element_1 in reversed(list(enumerate(first_sentence_tokens))):
        for index_2, element_2 in reversed(list(enumerate(second_sentence_tokens))):
            if element_1 == element_2:
                lcs.append(element_1)
                index_1 -= 1
                index_2 -= 2
            elif lcs_matrix[index_1 - 1][index_2] > lcs_matrix[index_1][index_2 - 1]:
                index_1 -= 1
            else:
                index_2 -= 1
    return tuple(lcs[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int) \
            or not isinstance(suspicious_sentence_tokens, tuple):
        return -1
    if len(suspicious_sentence_tokens) == 0:
        return 0

    if len(suspicious_sentence_tokens) < lcs_length \
            or lcs_length < 0 or isinstance(lcs_length, bool):
        return -1

    for word in suspicious_sentence_tokens:
        if not isinstance(word, str):
            return -1

    score = lcs_length / len(suspicious_sentence_tokens)

    return score


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
    if not isinstance(original_text_tokens, tuple) or \
            not all(isinstance(i, tuple) for i in original_text_tokens) or \
            not all(isinstance(i, str) for token in original_text_tokens for i in token):
        return -1

    if not isinstance(suspicious_text_tokens, tuple) or \
            not all(isinstance(i, tuple) for i in suspicious_text_tokens) or \
            not all(isinstance(i, str) for token in suspicious_text_tokens for i in token):
        return -1

    if len(suspicious_text_tokens) > len(original_text_tokens):
        original_text_tokens = list(original_text_tokens)
        while len(suspicious_text_tokens) > len(original_text_tokens):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    score_sum = 0

    for ind, token in enumerate(suspicious_text_tokens):
        lcs = find_lcs_length(original_text_tokens[ind], token, plagiarism_threshold)
        score = calculate_plagiarism_score(lcs, token)
        score_sum += score

    return score_sum / len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    check1 = (not isinstance(original_sentence_tokens, tuple) or
              not isinstance(suspicious_sentence_tokens, tuple) or
              not all(isinstance(i, str) for i in original_sentence_tokens) or
              not all(isinstance(i, str) for i in suspicious_sentence_tokens))

    check2 = (not isinstance(lcs, tuple) or
              not all(isinstance(i, str) for i in lcs))

    if check1 or check2:
        return ()

    sentences = (original_sentence_tokens, suspicious_sentence_tokens)
    diff = []

    for sentence in sentences:
        diff1 = []
        for i, token in enumerate(sentence):
            if token not in lcs:
                if i == 0 or sentence[i - 1] in lcs:
                    diff1.append(i)
                if i == len(sentence) - 1 or sentence[i + 1] in lcs:
                    diff1.append(i + 1)
        diff.append(tuple(diff1))

    return tuple(diff)


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

    text_plagiarism = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens,
                                                                    plagiarism_threshold)

    diff_stats = {'text_plagiarism': text_plagiarism, 'sentence_plagiarism': [], 'sentence_lcs_length': [],
                  'difference_indexes': []}

    for original_sentence, suspicious_sentence in zip(original_text_tokens, suspicious_text_tokens):
        lcs_length = find_lcs_length(original_sentence, suspicious_sentence, plagiarism_threshold)
        diff_stats['sentence_lcs_length'].append(lcs_length)
        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_sentence)
        lcs_matrix = fill_lcs_matrix(original_sentence, suspicious_sentence)
        lcs = find_lcs(original_sentence, suspicious_sentence, lcs_matrix)
        sent_diff = find_diff_in_sentence(original_sentence, suspicious_sentence, lcs)
        if plagiarism_score == -1:
            plagiarism_score = 0
        diff_stats['sentence_plagiarism'].append(plagiarism_score)
        diff_stats['difference_indexes'].append(sent_diff)
    return diff_stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    check_type = (not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple))
    if check_type or not isinstance(accumulated_diff_stats, dict):
        return ''

    texts_length = len(original_text_tokens)
    result_stats = ''

    for sent_ind in range(texts_length):
        orig_sentence = list(original_text_tokens[sent_ind])
        susp_sentence = list(suspicious_text_tokens[sent_ind])
        difference_indexes = accumulated_diff_stats['difference_indexes'][sent_ind]

        insert_number = 0
        for index in difference_indexes[0]:
            orig_sentence.insert(index + insert_number, '|')
            susp_sentence.insert(index + insert_number, '|')
            insert_number += 1

        orig_sentence = ' '.join(orig_sentence)
        susp_sentence = ' '.join(susp_sentence)

        lcs = accumulated_diff_stats['sentence_lcs_length'][sent_ind]
        sentence_plagiarism = float(accumulated_diff_stats['sentence_plagiarism'][sent_ind] * 100)
        result_stats += '- {}\n+ {}\n\nlcs = {}, plagiarism = {}%\n\n'.format(orig_sentence,
                                                                              susp_sentence,
                                                                              lcs,
                                                                              sentence_plagiarism)
    text_plagiarism = float(accumulated_diff_stats['text_plagiarism'] * 100)
    result_stats += 'Text average plagiarism (words): {}%'.format(text_plagiarism)

    return result_stats


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
    return 0


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    return ()
