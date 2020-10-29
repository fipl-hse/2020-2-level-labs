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
    sent_list = []
    if not isinstance(text, str):
        return ()
    new_text = ""
    text = text.lower()
    extra = set("""1234567890-=!@#$%^&*()_+,./<>?;:'"[{}]"'""")
    for letter in text:
        if letter not in extra:
            new_text += letter
    new_text = new_text.split('\n')
    for sent in new_text:
        sent = tokenize(sent)
        if sent:
            sent_list.append(tuple(sent))

    return tuple(sent_list)


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not isinstance(rows, int) or not isinstance(columns, int):
        return []
    if str(type(rows)) == "<class 'bool'>" or str(type(columns)) == "<class 'bool'>":
        return []
    if rows is None or columns is None:
        return []
    if rows <= 0 or columns <= 0:
        return []
    return [[0 for j in range(columns)] for i in range(rows)]


def create_big_zero_matrix(rows, columns):
    return create_zero_matrix(rows + 1, columns + 1)


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not first_sentence_tokens or not second_sentence_tokens \
            or str(type(first_sentence_tokens)) == "<class 'bool'>":
        return []

    if str(type(second_sentence_tokens)) == "<class 'bool'>" \
            or first_sentence_tokens is None or second_sentence_tokens is None:
        return []
    
    for token in first_sentence_tokens:
        if not isinstance(token, str) and not isinstance(token, int) or \
                str(type(token)) == "<class 'bool'>" or str(type(token)) == "<class 'bool'>" or \
                token is None:
            return []

    for token in second_sentence_tokens:
        if not isinstance(token, str) and not isinstance(token, int) or \
                str(type(token)) == "<class 'bool'>" or str(type(token)) == "<class 'bool'>" or \
                token is None:
            return []

    f_lcs_matrix = create_big_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    first_iterations = len(first_sentence_tokens)
    second_iterations = len(second_sentence_tokens)
    for i in range(first_iterations):
        for j in range(second_iterations):
            if first_sentence_tokens[i] == second_sentence_tokens[j]:
                f_lcs_matrix[i + 1][j + 1] = f_lcs_matrix[i][j] + 1
            else:
                f_lcs_matrix[i + 1][j + 1] = max(f_lcs_matrix[i][j + 1], f_lcs_matrix[i + 1][j])

    del f_lcs_matrix[0]

    for line in f_lcs_matrix:
        del line[0]

    return f_lcs_matrix


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not isinstance(lcs_matrix,
                              list) or not first_sentence_tokens or not second_sentence_tokens or not lcs_matrix:
        return ()

    if first_sentence_tokens[0] is None or not all(isinstance(w, str) for w in first_sentence_tokens):
        return ()

    if second_sentence_tokens[0] is None or not all(isinstance(w, str) for w in second_sentence_tokens):
        return ()

    if not lcs_matrix or not isinstance(lcs_matrix, list) or not all(
            isinstance(i, list) for i in lcs_matrix) or not all(isinstance(i, int) \
                                                                for lists in lcs_matrix for i in lists):
        return ()

    if lcs_matrix != fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens):
        return ()

    answer = []

    lcs_matrix.insert(0, [0 for i in range(len(lcs_matrix[0]))])

    for line in lcs_matrix:
        line.insert(0, 0)

    i = len(lcs_matrix) - 1
    j = len(lcs_matrix[0]) - 1

    while i >= 1 and j >= 1:
        if first_sentence_tokens[i - 1] == second_sentence_tokens[j - 1]:
            answer.append(first_sentence_tokens[i - 1])
            i -= 1
            j -= 1
        else:
            if lcs_matrix[i - 1][j] > lcs_matrix[i][j - 1]:
                i -= 1
            else:
                j -= 1

    del lcs_matrix[0]

    for line in lcs_matrix:
        del line[0]

    return tuple(answer.__reversed__())


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """

    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or not isinstance(
            plagiarism_threshold, float):
        return -1

    if not 0 <= plagiarism_threshold <= 1:
        return -1

    for token in first_sentence_tokens:
        if not isinstance(token, str) and not isinstance(token, int):
            return -1

    for token in second_sentence_tokens:
        if not isinstance(token, str) and not isinstance(token, int):
            return -1
    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return 0

    new_lcs = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)

    i = len(new_lcs) - 1
    j = len(new_lcs[0]) - 1
    return new_lcs[i][j]


def plagiarism(first_line: tuple, second_line: tuple) -> float:
    lcs_find = find_lcs_length(first_line, second_line, 0.0)
    res = calculate_plagiarism_score(lcs_find, second_line)
    return res


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if str(type(lcs_length)) == "<class 'bool'>" or not isinstance(lcs_length, int) or lcs_length is None \
            or not isinstance(suspicious_sentence_tokens, tuple) or suspicious_sentence_tokens is None:
        return -1

    for token in suspicious_sentence_tokens:
        if not isinstance(token, str):
            return -1

    if len(suspicious_sentence_tokens) == 0:
        return 0

    if not 0 <= lcs_length <= len(suspicious_sentence_tokens):
        return -1

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

    if (str(type(original_text_tokens)) == "<class 'bool'>" \
        or str(type(suspicious_text_tokens)) == "<class 'bool'>") or \
            original_text_tokens is None \
            or suspicious_text_tokens is None or original_text_tokens == (None, None) \
            or suspicious_text_tokens == (None, None) \
            or not isinstance(original_text_tokens, tuple) \
            or not isinstance(suspicious_text_tokens,
                              tuple):
        return -1

    for second_element in original_text_tokens:
        if not isinstance(second_element, tuple):
            return -1
        for element in second_element:
            if not isinstance(element, str):
                return -1

    for second_element in suspicious_text_tokens:
        if not isinstance(second_element, tuple):
            return -1
        for element in second_element:
            if not isinstance(element, str):
                return -1

    if plagiarism_threshold is None or str(type(plagiarism_threshold)) == "<class 'bool'>" \
            or not isinstance(plagiarism_threshold, float) \
            or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1

    summa = 0
    for lines in zip(original_text_tokens, suspicious_text_tokens):
        summa += plagiarism(lines[0], lines[1])
    return summa / len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """

    if not isinstance(original_sentence_tokens, tuple) or not isinstance(suspicious_sentence_tokens, tuple) \
            or not isinstance(lcs, tuple):
        return ()

    for element in original_sentence_tokens:
        if not isinstance(element, str):
            return ()

    for element in suspicious_sentence_tokens:
        if not isinstance(element, str):
            return ()

    for element in lcs:
        if not isinstance(element, str):
            return ()

    og_sent = []
    sus_sent = []
    i = 0
    j = 0
    while j < len(lcs) or i < len(original_sentence_tokens):
        if j < len(lcs) and original_sentence_tokens[i] == lcs[j]:
            j += 1
        else:
            og_sent.append(i)
        i += 1

    i = 0
    j = 0

    while j < len(lcs) or i < len(suspicious_sentence_tokens):
        if j < len(lcs) and suspicious_sentence_tokens[i] == lcs[j]:
            j += 1
        else:
            sus_sent.append(i)

        i += 1

    res1 = []

    prev = -100
    iterations = len(og_sent)
    for i in range(iterations):
        if og_sent[i] - prev != 1:
            res1.append(og_sent[i])
            if i + 1 < len(og_sent) and og_sent[i + 1] - og_sent[i] != 1:
                res1.append(og_sent[i] + 1)
            elif i == len(og_sent) - 1 and og_sent[i] < len(original_sentence_tokens):
                res1.append(og_sent[i] + 1)
        else:
            if i + 1 < len(og_sent) and og_sent[i + 1] - og_sent[i] != 1:
                res1.append(og_sent[i + 1])
            elif i + 1 == len(og_sent):
                res1.append(og_sent[i] + 1)
        prev = og_sent[i]

    res2 = []
    prev = -100
    iterations = len(sus_sent)
    for i in range(iterations):
        if sus_sent[i] - prev != 1:
            res2.append(sus_sent[i])
            if i + 1 < len(sus_sent) and sus_sent[i + 1] - sus_sent[i] != 1:
                res2.append(sus_sent[i] + 1)
            elif i == len(sus_sent) - 1 and sus_sent[i] < len(suspicious_sentence_tokens):
                res2.append(sus_sent[i] + 1)
        else:
            if i + 1 < len(sus_sent) and sus_sent[i + 1] - sus_sent[i] != 1:
                res2.append(sus_sent[i + 1])
            elif i + 1 == len(sus_sent):
                res2.append(sus_sent[i] + 1)
        prev = sus_sent[i]

    return tuple(res1), tuple(res2)


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

    res_dict = {}

    text_plagiarism = calculate_text_plagiarism_score(
        original_text_tokens,
        suspicious_text_tokens,
        plagiarism_threshold=0.3
    )

    res_dict['text_plagiarism'] = text_plagiarism
    sentence_plagiarism = []
    for lines in zip(original_text_tokens, suspicious_text_tokens):
        sentence_plagiarism.append(plagiarism(lines[0], lines[1]))
    res_dict['sentence_plagiarism'] = sentence_plagiarism

    sentence_lcs_length = []
    for lines in zip(original_text_tokens, suspicious_text_tokens):
        sentence_lcs_length.append(find_lcs_length(lines[0], lines[1], plagiarism_threshold))
    res_dict['sentence_lcs_length'] = sentence_lcs_length

    difference_indexes = []
    for lines in zip(original_text_tokens, suspicious_text_tokens):
        difference_indexes.append(
            find_diff_in_sentence(
                lines[0],
                lines[1],
                find_lcs(
                    lines[0],
                    lines[1],
                    fill_lcs_matrix(lines[0], lines[1])
                )
            )
        )

    res_dict['difference_indexes'] = difference_indexes
    return res_dict


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    line_number = 0
    result = ''
    avarage = 0
    for line in zip(original_text_tokens, suspicious_text_tokens):
        result += '- '
        i = 0
        j = 0
        for token in line[0]:
            if j < len(accumulated_diff_stats['difference_indexes'][line_number][0]) \
                    and accumulated_diff_stats['difference_indexes'][line_number][0][j] == i:
                result += '| '
                j += 1
            result += token + ' '
            i += 1
        result += '\n'
        result += '+ '
        i = 0
        j = 0
        for token in line[1]:
            if j < len(accumulated_diff_stats['difference_indexes'][line_number][1]) \
                    and accumulated_diff_stats['difference_indexes'][line_number][1][j] == i:
                result \
                    += '| '
                j += 1
            result += token + ' '
            i += 1
        line_number += 1
        result += '\n'
        result += '\n'
        lcs = find_lcs_length(line[0], line[1], 0.3)
        result += 'lcs = ' + str(lcs) + ', '
        plagiate = calculate_plagiarism_score(lcs, line[1])
        avarage += plagiate
        result += 'plagiarism = ' + str(plagiate * 100) + '%'
        result += '\n'
        result += '\n'
    avarage /= len(suspicious_text_tokens)
    result += 'Text average plagiarism (words): ' + str(avarage * 100) + '%'
    return result


def find_lcs_length_optimized(first_sentence_tokens: list, second_sentence_tokens: list) -> int:
    """
    Finds a length of the longest common subsequence using the Hirschberg's algorithm
    At the same time, if the first and last tokens coincide,
    they are immediately added to lcs and not analyzed
    :param first_sentence_tokens: a list of tokens
    :param second_sentence_tokens: a list of tokens
    :return: a length of the longest common subsequence
    """
    pass


def tokenize_big_file(path_to_file: str) -> tuple:
    pass
