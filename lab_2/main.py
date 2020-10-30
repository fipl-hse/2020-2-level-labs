"""
Main.py
"""

from tokenizer import tokenize

def tokenize_by_lines(text: str) -> tuple:
    if not isinstance(text, str):
        return ()

    sentences = text.split('\n')
    tokens_from_text = [tuple(tokenize(sent)) for sent in sentences]
    tokens_from_sent = tuple([sent for sent in tokens_from_text if sent])
    return tokens_from_sent


def create_zero_matrix(rows: int, columns: int) -> list:
    checks = (not isinstance(rows, int) or isinstance(rows, bool) or not isinstance(columns, int)
              or isinstance(columns, bool) or rows <= 0 or columns <= 0)

    if checks:
        return []

    matrix = [[0] * columns for row in range(rows)]
    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    checks = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)
              or not all(isinstance(token, str) for token in first_sentence_tokens)
              or not all(isinstance(token, str) for token in second_sentence_tokens))

    if checks:
        return []

    matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    for index1, word1 in enumerate(first_sentence_tokens):
        for index2, word2 in enumerate(second_sentence_tokens):
            if word1 == word2:
                matrix[index1][index2] = max(matrix[index1 - 1][index2], matrix[index1][index2 - 1]) + 1
            else:
                matrix[index1][index2] = max(matrix[index1 - 1][index2], matrix[index1][index2 - 1])

    return matrix


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    checks = (not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)
              or not isinstance(plagiarism_threshold, float) or plagiarism_threshold < 0 or plagiarism_threshold > 1
              or not all(isinstance(token, str) for token in first_sentence_tokens)
              or not all(isinstance(token, str) for token in second_sentence_tokens))

    if checks:
        return -1

    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return 0

    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    length = matrix[- 1][- 1]

    if length / len(second_sentence_tokens) < plagiarism_threshold:
        return 0

    return length

def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    checks = (not isinstance(first_sentence_tokens, tuple) or len(first_sentence_tokens) == 0
              or not all(isinstance(token, str) for token in first_sentence_tokens)
              or not isinstance(second_sentence_tokens, tuple) or len(second_sentence_tokens) == 0
              or not all(isinstance(token, str) for token in second_sentence_tokens)
              or not lcs_matrix or not isinstance(lcs_matrix, list)
              or not all(isinstance(i, list) for i in lcs_matrix)
              or not lcs_matrix[0][0] in (0, 1) or not len(lcs_matrix) == len(first_sentence_tokens))

    if checks:
        return ()

    lcs = []

    row = len(lcs_matrix) - 1
    column = len(lcs_matrix[0]) - 1

    while row and column:
        row_1 = lcs_matrix[row - 1][column] if row - 1 >= 0 else 0
        column_1 = lcs_matrix[row][column - 1] if column - 1 >= 0 else 0
        if first_sentence_tokens[row] == second_sentence_tokens[column]:
            lcs += [first_sentence_tokens[row]]
            row -= 1
            column -= 1
        elif row_1 > column_1:
            row -= 1
        else:
            column -= 1

    if first_sentence_tokens[0] == second_sentence_tokens[0]:
        lcs += [first_sentence_tokens[0]]

    lcs = tuple(lcs[::-1])

    return lcs

def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    if not isinstance(lcs_length, int) or not isinstance(suspicious_sentence_tokens, tuple):
        return -1
    if not suspicious_sentence_tokens:
        return 0
    if len(suspicious_sentence_tokens) < lcs_length or lcs_length < 0 or isinstance(lcs_length, bool) \
        or not all(isinstance(token, str) for token in suspicious_sentence_tokens):
        return -1

    return lcs_length / len(suspicious_sentence_tokens)


def calculate_text_plagiarism_score(original_text_tokens: tuple,
                                    suspicious_text_tokens: tuple, plagiarism_threshold=0.3) -> float:
    checks = (not isinstance(original_text_tokens, tuple)
              or not all(isinstance(tokens, tuple) for tokens in original_text_tokens)
              or not all(isinstance(token, str) for tokens in original_text_tokens for token in tokens)
              or not isinstance(suspicious_text_tokens, tuple)
              or not all(isinstance(tokens, tuple) for tokens in suspicious_text_tokens)
              or not all(isinstance(token, str) for tokens in suspicious_text_tokens for token in tokens)
              or not isinstance(plagiarism_threshold, float)
              or len(suspicious_text_tokens) <= 0)

    if checks:
        return -1

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens = list(original_text_tokens)
        for _ in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_text_tokens += [[]]
        original_text_tokens = tuple(original_text_tokens)

    plagiarism = 0

    for index, suspicious_sentence in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[index], suspicious_sentence, plagiarism_threshold)
        plagiarism += calculate_plagiarism_score(lcs_length, suspicious_sentence)

    text_plagiarism_score = plagiarism / len(suspicious_text_tokens)

    return text_plagiarism_score


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    checks = (not isinstance(original_sentence_tokens, tuple)
              or not isinstance(suspicious_sentence_tokens, tuple)
              or not isinstance(lcs, tuple)
              or not all(isinstance(token, str) for token in original_sentence_tokens)
              or not all(isinstance(token, str) for token in suspicious_sentence_tokens)
              or not all(isinstance(s, str) for s in lcs))

    if checks:
        return ()

    all_diff = []

    for sentence in (original_sentence_tokens, suspicious_sentence_tokens):
        diff = []
        for index, token in enumerate(sentence):
            if token not in lcs:
                if index == 0 or sentence[index - 1] in lcs:
                    diff += [index]
                if index == len(sentence) - 1 or sentence[index + 1] in lcs:
                    diff += [index + 1]
        all_diff += [tuple(diff)]

    return tuple(all_diff)


def accumulate_diff_stats(original_text_tokens: tuple, suspicious_text_tokens: tuple, plagiarism_threshold=0.3) -> dict:
    checks = (not isinstance(original_text_tokens, tuple)
              or not isinstance(suspicious_text_tokens, tuple)
              or plagiarism_threshold < 0 or plagiarism_threshold > 1)

    if checks:
        return {}

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += [[]] * (len(suspicious_text_tokens) - len(original_text_tokens))

    text_plagiarism = calculate_text_plagiarism_score(original_text_tokens,
                                                      suspicious_text_tokens, plagiarism_threshold)

    stats = {'text_plagiarism': text_plagiarism,
             'sentence_plagiarism': [],
             'sentence_lcs_length': [],
             'difference_indexes': []}

    for original_sentence, suspicious_sentence in zip(original_text_tokens, suspicious_text_tokens):
        stats['sentence_plagiarism'] += [calculate_plagiarism_score(find_lcs_length(original_sentence,
                                                                                    suspicious_sentence,
                                                                                    plagiarism_threshold),
                                                                                    suspicious_sentence)]
        stats['sentence_lcs_length'] += [find_lcs_length(original_sentence, suspicious_sentence, plagiarism_threshold)]
        stats['difference_indexes'] += [find_diff_in_sentence(original_sentence, suspicious_sentence,
                                                              find_lcs(original_sentence, suspicious_sentence,
                                                              fill_lcs_matrix(original_sentence, suspicious_sentence)))]

    return stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    checks = (not isinstance(original_text_tokens, tuple)
              or not isinstance(suspicious_text_tokens, tuple)
              or not isinstance(accumulated_diff_stats, dict))

    if checks:
        return ''

    len_orig = len(original_text_tokens)
    report = ''

    for sent_index in range(len_orig):
        original_sentence = list(original_text_tokens[sent_index])
        suspicious_sentence = list(suspicious_text_tokens[sent_index])
        diff = accumulated_diff_stats['difference_indexes'][sent_index]

        insert_number = 0
        for index in diff[0]:
            original_sentence.insert(index + insert_number, '|')
            suspicious_sentence.insert(index + insert_number, '|')
            insert_number += 1

        original_sentence = ' '.join(original_sentence)
        suspicious_sentence = ' '.join(suspicious_sentence)

        lcs = accumulated_diff_stats['sentence_lcs_length'][sent_index]
        sentence_plagiarism = float(accumulated_diff_stats['sentence_plagiarism'][sent_index] * 100)
        report += '- {}\n+ {}\nlcs = {}, plagiarism = {}%\n'.format(original_sentence,
                                                                    suspicious_sentence,
                                                                    lcs,
                                                                    sentence_plagiarism)

    report += 'Text average plagiarism (words): {}%'.format(float(accumulated_diff_stats['text_plagiarism'] 
                                                                  * 100))

    return report


def find_lcs_length_optimized(first_sentence_tokens: tuple, second_sentence_tokens: tuple,
                              plagiarism_threshold: float) -> int:
    return 0


def tokenize_big_file(path_to_file: str, ids=0) -> tuple:
    return ()
