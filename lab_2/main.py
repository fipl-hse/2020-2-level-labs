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

    tokens = ()

    if not isinstance(text, str):
        return ()

    sentences = text.split('\n')
    tokens = tuple(tuple(tokenizer.tokenize(sentence)) for sentence in sentences if tokenizer.tokenize(sentence))
    return tokens


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    check = [isinstance(rows, int) and isinstance(columns, int) and not isinstance(rows, bool) and not isinstance(columns, bool)]

    if not all(check) or rows < 1 or columns < 1:
        return []

    matrix = []

    for row in range(rows):
        matrix.append([0*i for i in range(columns)])

    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    check = [isinstance(first_sentence_tokens, tuple), isinstance(second_sentence_tokens, tuple),
             first_sentence_tokens, second_sentence_tokens]

    if all(check) and all(isinstance(word, str) for word in first_sentence_tokens)\
            and all(isinstance(word, str) for word in second_sentence_tokens):

        matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

        for i, xi in enumerate(first_sentence_tokens):
            for j, yj in enumerate(second_sentence_tokens):

                if xi == yj:
                    if (i - 1) < 0 or (j - 1) < 0:
                        matrix[i][j] = 1
                    else:
                        matrix[i][j] = matrix[i - 1][j - 1] + 1

                else:
                    if (i - 1) < 0 and (i - 1) > 0:
                        matrix[i][j] = matrix[i][j - 1]
                    elif (i - 1) > 0 and (j - 1) < 0:
                        matrix[i][j] = matrix[i - 1][j]
                    elif (i - 1) < 0 and (j - 1) < 0:
                        matrix[i][j] = 0
                    else:
                        matrix[i][j] = max(matrix[i][j - 1], matrix[i - 1][j])

        return matrix
    return []


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """

    fst_check = not ((isinstance(first_sentence_tokens, tuple) and first_sentence_tokens
                     and first_sentence_tokens[0] is not None)
                     or (isinstance(first_sentence_tokens, tuple) and not first_sentence_tokens))
    sst_check = not ((isinstance(second_sentence_tokens, tuple) and second_sentence_tokens
                     and second_sentence_tokens[0] is not None)
                     or (isinstance(second_sentence_tokens, tuple) and not second_sentence_tokens))
    threshold_check = ((isinstance(plagiarism_threshold, int) or isinstance(plagiarism_threshold, float))
                       and not isinstance(plagiarism_threshold, bool) and 0 < plagiarism_threshold < 1)

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)

    if fst_check or sst_check or not threshold_check:
        return -1

    if not first_sentence_tokens or not second_sentence_tokens:
        return 0

    lcs_length = lcs_matrix[-1][-1] if lcs_matrix else 0
    if lcs_length and lcs_length / len(second_sentence_tokens) < plagiarism_threshold:
        return 0

    return lcs_matrix[-1][-1]


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    fst_check = (not isinstance(first_sentence_tokens, tuple) or not first_sentence_tokens
                 or len(first_sentence_tokens) == 0 or first_sentence_tokens[0] is None
                 or not all(isinstance(word, str) for word in first_sentence_tokens))
    sst_check = (not isinstance(second_sentence_tokens, tuple) or not second_sentence_tokens
                 or len(second_sentence_tokens) == 0 or second_sentence_tokens[0] is None
                 or not all(isinstance(word, str) for word in second_sentence_tokens))

    if fst_check or sst_check:
        return ()

    matrix_check = (not lcs_matrix or not isinstance(lcs_matrix, list)
                    or not all(isinstance(i, list) for i in lcs_matrix)
                    or not all(isinstance(i, int) for lists in lcs_matrix for i in lists)
                    or not lcs_matrix[0][0] in (0, 1)
                    or not len(lcs_matrix) == len(first_sentence_tokens)
                    or not len(lcs_matrix[0]) == len(second_sentence_tokens))

    if matrix_check:
        return ()

    row = len(lcs_matrix) - 1
    column = len(lcs_matrix[0]) - 1

    lcs = []

    while row or column:
        top = lcs_matrix[row - 1][column] if row - 1 >= 0 else 0
        left = lcs_matrix[row][column - 1] if column - 1 >= 0 else 0
        if first_sentence_tokens[row] == second_sentence_tokens[column]:
            lcs.append(first_sentence_tokens[row])
            row -= 1
            column -= 1
        elif top > left or not column:
            row -= 1
        else:
            column -= 1

    if first_sentence_tokens[0] == second_sentence_tokens[0]:
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

    if not isinstance(suspicious_sentence_tokens, tuple)\
            or not all(isinstance(token, str) for token in suspicious_sentence_tokens):
        return -1

    if len(suspicious_sentence_tokens) == 0:
        return 0

    if not (not isinstance(lcs_length, bool) and isinstance(lcs_length, int)
            and 0 <= lcs_length <= len(suspicious_sentence_tokens)):
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
    original_check = (not isinstance(original_text_tokens, tuple)
                      or not all(isinstance(i, tuple) for i in original_text_tokens)
                      or not all(isinstance(i, str) for tokens in original_text_tokens for i in tokens))

    suspicious_check = (not isinstance(suspicious_text_tokens, tuple)
                        or not all(isinstance(i, tuple) for i in suspicious_text_tokens)
                        or not all(isinstance(i, str) for tokens in suspicious_text_tokens for i in tokens))

    threshold_check = (not isinstance(plagiarism_threshold, float)
                       or not (0 < plagiarism_threshold < 1))

    if ((isinstance(original_text_tokens, tuple) and not any(original_text_tokens))
            or (isinstance(suspicious_text_tokens, tuple) and not any(suspicious_text_tokens))):
        return 0

    if original_check or suspicious_check or threshold_check:
        return -1

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens = list(original_text_tokens)
        for i in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    plagiarism = 0

    for i, suspicious_sentence in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[i], suspicious_sentence, plagiarism_threshold)
        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_sentence)
        plagiarism += plagiarism_score

    return plagiarism / len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    sentences_check = not (isinstance(original_sentence_tokens, tuple)
                           and isinstance(suspicious_sentence_tokens, tuple)
                           and all(isinstance(i, str) for i in original_sentence_tokens)
                           and all(isinstance(i, str) for i in suspicious_sentence_tokens))
    lcs_check = not (isinstance(lcs, tuple)
                     and all(isinstance(i, str) for i in lcs))

    if sentences_check or lcs_check:
        return ()

    diff_sum = []

    for sentence in (original_sentence_tokens, suspicious_sentence_tokens):

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
    original_check = not (isinstance(original_text_tokens, tuple)
                          and all(isinstance(i, tuple) for i in original_text_tokens)
                          and all(isinstance(i, str) for tokens in original_text_tokens for i in tokens))
    suspicious_check = not (isinstance(suspicious_text_tokens, tuple)
                            and all(isinstance(i, tuple) for i in suspicious_text_tokens)
                            and all(isinstance(i, str) for tokens in suspicious_text_tokens for i in tokens))

    if original_check or suspicious_check\
            or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return {}

    text_plagiarism = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    stats = {'text_plagiarism': text_plagiarism, 'sentence_plagiarism': [], 'sentence_lcs_length': [], 'difference_indexes': []}

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens = list(original_text_tokens)
        for i in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    for original_sentence, suspicious_sentence in zip(original_text_tokens, suspicious_text_tokens):
        lcs_length = find_lcs_length(original_sentence, suspicious_sentence, plagiarism_threshold)
        stats['sentence_lcs_length'].append(lcs_length)
        stats['sentence_plagiarism'].append(calculate_plagiarism_score(lcs_length, suspicious_sentence))
        lcs_matrix = fill_lcs_matrix(original_sentence, suspicious_sentence)
        lcs = find_lcs(original_sentence, suspicious_sentence, lcs_matrix)
        stats['difference_indexes'].append(find_diff_in_sentence(original_sentence, suspicious_sentence, lcs))

    return stats


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
        original_text_tokens = list(original_text_tokens)
        for i in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    def sentence_with_lines(sentences, index):
        for i in range(0, len(index), 2):
            if index[i] + 1 == index[i + 1]:
                sentences[index[i]] = f'| {sentences[index[i]]} |'
            else:
                sentences[index[i]] = f'| {sentences[index[i]]}'
                sentences[index[i + 1]] = f'{sentences[index[i + 1] - 1]} |'
        return ' '. join(sentences)

    report = ''

    for i, (original_i, suspicious_i) in enumerate(
            accumulated_diff_stats['difference_indexes']):
        original = list(original_text_tokens)
        suspicious = list(suspicious_text_tokens)
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
    pass


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    if not isinstance(path_to_file, str):
        return ()

