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

    if not isinstance(text, str):
        return ()

    tokens = []
    sentences = text.split('\n')
    for elems in sentences:
        tokenized_text = tuple(tokenizer.tokenize(elems))
        if tokenized_text:
            tokens.append(tokenized_text)
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
    is_rows = not isinstance(rows, int) or isinstance(rows, bool)
    is_cols = not isinstance(columns, int) or isinstance(columns, bool)

    if is_rows or is_cols or rows <= 0 or columns <= 0:
        return []

    zero_matrix = []
    for i in range(rows):
        zero_matrix.append([0] * columns)
    return zero_matrix


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

    mtx = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    for idx1, elem1 in enumerate(first_sentence_tokens):
        for idx2, elem2 in enumerate(second_sentence_tokens):
            if elem1 == elem2:
                mtx[idx1][idx2] = mtx[idx1 - 1][idx2 - 1] + 1
            else:
                mtx[idx1][idx2] = max(mtx[idx1][idx2 - 1], mtx[idx1 - 1][idx2])
    return mtx


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    token_check = (not isinstance(first_sentence_tokens, tuple)
                   or not isinstance(second_sentence_tokens, tuple)
                   or not all(isinstance(i, str) for i in first_sentence_tokens)
                   or not all(isinstance(i, str) for i in second_sentence_tokens))

    float_check = (not isinstance(plagiarism_threshold, float) and not 1 > plagiarism_threshold > 0)

    if token_check or float_check:
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
    else:
        return lcs_len


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """

    token_check = (not isinstance(first_sentence_tokens, tuple)
                   or not isinstance(second_sentence_tokens, tuple)
                   or not all(isinstance(i, str) for i in first_sentence_tokens)
                   or not all(isinstance(i, str) for i in second_sentence_tokens))

    list_check = (not isinstance(lcs_matrix, list)
                  or not lcs_matrix
                  or not all(isinstance(i, list) for i in lcs_matrix)
                  or not all(isinstance(i, int) for sublist in lcs_matrix for i in sublist)
                  or all(isinstance(i, bool) for sublist in lcs_matrix for i in sublist))

    if token_check or list_check or not(lcs_matrix[0][0] == 0 or lcs_matrix[0][0] == 1):
        return ()

    index_1 = len(first_sentence_tokens) - 1
    index_2 = len(second_sentence_tokens) - 1
    lcs = []

    while len(lcs) != lcs_matrix[-1][-1] and index_1 >= 0 and index_2 >= 0:
        if index_1 > 0:
            cell_1 = lcs_matrix[index_1 - 1][index_2]
        if index_2 > 0:
            cell_2 = lcs_matrix[index_1][index_2 - 1]
        if index_1 != 0 and index_2 == 0:
            index_1 = 0
        if first_sentence_tokens[index_1] == second_sentence_tokens[index_2]:
            lcs.append(first_sentence_tokens[index_1])
            index_1 -= 1
            index_2 -= 1
        elif cell_1 > cell_2:
            index_1 -= 1
        else:
            index_2 -= 1
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
    len_check = not isinstance(lcs_length, int) or isinstance(lcs_length, bool)

    susp_check = (not isinstance(suspicious_sentence_tokens, tuple)
                  or not all(isinstance(i, str) for i in suspicious_sentence_tokens))

    if isinstance(suspicious_sentence_tokens, tuple) and not suspicious_sentence_tokens:
        return 0

    if len_check or susp_check or not 0 <= lcs_length <= len(suspicious_sentence_tokens):
        return -1

    return lcs_length / len(suspicious_sentence_tokens)


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple, plagiarism_threshold=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    orig_check = (not isinstance(original_text_tokens, tuple)
                  or not all(isinstance(i, tuple) for i in original_text_tokens)
                  or not all(isinstance(i, str) for subtuple in original_text_tokens for i in subtuple))

    susp_check = (not isinstance(suspicious_text_tokens, tuple)
                  or not all(isinstance(i, tuple) for i in suspicious_text_tokens)
                  or not all(isinstance(i, str) for subtuple in suspicious_text_tokens for i in subtuple))

    plag_check = not isinstance(plagiarism_threshold, float) or plagiarism_threshold < 0 or plagiarism_threshold > 1

    if (isinstance(original_text_tokens, tuple) and not any(original_text_tokens) or
            isinstance(suspicious_text_tokens, tuple) and not any(suspicious_text_tokens)):
        return 0

    if orig_check or susp_check or plag_check:
        return -1

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens = list(original_text_tokens)
        for i in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    p_scores = 0

    for i, susp_sentence in enumerate(suspicious_text_tokens):
        lcs_len = find_lcs_length(original_text_tokens[i], susp_sentence, plagiarism_threshold)
        p_score = calculate_plagiarism_score(lcs_len, susp_sentence)
        p_scores += p_score

    return p_scores / len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
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
        for i in range(len(susp) - len(orig)):
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


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    orig = original_text_tokens
    susp = suspicious_text_tokens

    orig_check = not (isinstance(orig, tuple)
                          and all(isinstance(i, tuple) for i in orig)
                          and all(isinstance(i, str) for tokens in orig for i in tokens))
    susp_check = not (isinstance(susp, tuple)
                            and all(isinstance(i, tuple) for i in susp)
                            and all(isinstance(i, str) for tokens in susp for i in tokens))

    if orig_check or susp_check or not isinstance(accumulated_diff_stats, dict):
        return ''

    if len(orig) < len(susp):
        add = (len(susp) - len(orig))
        while add > 0:
            orig = list(orig)
            orig.append(('',))
            add -= 1
        orig = tuple(orig)

    report = ''
    for sentence_index in range(len(susp)):
        if accumulated_diff_stats['difference_indexes'][sentence_index] == ((), ()):
            orig_sentence = ' '.join(orig[sentence_index])
            susp_sentence = ' '.join(susp[sentence_index])
        else:
            orig_sentence = list(orig[sentence_index])
            counter = 1
            for diff_words_index in accumulated_diff_stats['difference_indexes'][sentence_index][0]:
                if counter % 2 != 0:
                    orig_sentence.insert(diff_words_index, '|')
                    counter += 1
                else:
                    orig_sentence.insert(diff_words_index + 1, '|')
                    counter += 1
            orig_sentence = ' '.join(orig_sentence)

            susp_sentence = list(susp[sentence_index])
            counter = 1
            for diff_words_index in accumulated_diff_stats['difference_indexes'][sentence_index][1]:
                if counter % 2 != 0:
                    susp_sentence.insert(diff_words_index, '|')
                    counter += 1
                else:
                    susp_sentence.insert(diff_words_index + 1, '|')
                    counter += 1
            susp_sentence = ' '.join(susp_sentence)

        report += '- {}\n+ {}\n\nlcs = {}, plagiarism = {}%\n\n'.format(
            orig_sentence, susp_sentence, accumulated_diff_stats['sentence_lcs_length'][sentence_index],
            accumulated_diff_stats['sentence_plagiarism'][sentence_index] * 100)
    report += 'Text average plagiarism (words): {}%\n\n'.format(accumulated_diff_stats['text_plagiarism'] * 100)


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
