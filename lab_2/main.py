"""
Longest common subsequence problem
"""


def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    if not isinstance(text, str) or not text:
        return tuple()

    separators = '.,?!":-<>(){}'
    lines = ["".join(char for char in line.lower() if char not in separators) for line in text.split('\n')]

    return tuple(tuple(line.split()) for line in lines if tuple(line.split()))

def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if (
            isinstance(rows, int) and isinstance(columns, int) \
            and (rows > 0 and columns > 0) \
            and (not isinstance(rows, bool) and not isinstance(columns, bool))
    ):
        return [[0 for col in range(columns)] for row in range(rows)]

    return []

def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if (
        not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
        or any(not isinstance(token, str) for token in first_sentence_tokens) \
        or any(not isinstance(token, str) for token in second_sentence_tokens) \
    ):
        return []
    
    if not first_sentence_tokens or not second_sentence_tokens:
        return []

    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for first_i, first in enumerate(first_sentence_tokens):
        for second_i, second in enumerate(second_sentence_tokens):
            if first == second:
                lcs_matrix[first_i][second_i] = lcs_matrix[first_i - 1][second_i - 1] + 1
            else:
                lcs_matrix[first_i][second_i] = max(
                        lcs_matrix[first_i][second_i - 1],
                        lcs_matrix[first_i - 1][second_i]
                )

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
    if (
        not isinstance(first_sentence_tokens, tuple) \
        or not isinstance(second_sentence_tokens, tuple) \
        or not isinstance(plagiarism_threshold, float) \
        or not 0 < plagiarism_threshold < 1
    ):
        return -1
    
    if (
        any(not isinstance(word, str) for word in first_sentence_tokens) \
        or any(not isinstance(word, str) for word in second_sentence_tokens) \
    ):
        return -1

    first, second = first_sentence_tokens, second_sentence_tokens
    if not len(first) or not len(second):
        return 0

    if len(first) > len(second):
        first, second = second, first

    lcs_matrix = fill_lcs_matrix(first, second)

    if not lcs_matrix:
        return -1

    lcs_length = lcs_matrix[-1][-1]

    if lcs_length / len(second) < plagiarism_threshold:
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
    if (
        not isinstance(first_sentence_tokens, tuple) \
        or not isinstance(second_sentence_tokens, tuple) \
        or not isinstance(lcs_matrix, list) \
        or not first_sentence_tokens or not second_sentence_tokens \
        or not len(lcs_matrix) == len(first_sentence_tokens) \
        or not sum(sum(element) for element in lcs_matrix) \
        or not lcs_matrix[0][0] in {0, 1}
    ):
        return tuple()

    first, second = first_sentence_tokens, second_sentence_tokens

    if len(first) > len(second):
        first, second = second, first

    if not first or not second:
        return 0

    first_index, second_index = len(first) - 1, len(second) - 1
    lcs = []

    while first_index >= 0 and second_index >= 0:
        if first[first_index] == second[second_index]:
            lcs.append(first[first_index])
            first_index -= 1
            second_index -= 1
        elif lcs_matrix[first_index - 1][second_index] > lcs_matrix[first_index][second_index - 1]:
            first_index -= 1
        else:
            second_index -= 1

    if lcs_matrix[0][0]:
        lcs.append(first[0])

    return tuple(lcs[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if (
        not isinstance(lcs_length, int) or isinstance(lcs_length, bool) \
        or not isinstance(suspicious_sentence_tokens, tuple) \
        or any(not isinstance(element, str) for element in suspicious_sentence_tokens) \
        or suspicious_sentence_tokens in [[], {}]
    ):
        return -1.0
    if not suspicious_sentence_tokens:
        return 0.0

    if not 0 <= lcs_length <= len(suspicious_sentence_tokens):
        return -1.0

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
    if (
        not isinstance(original_text_tokens, tuple) \
        or not isinstance(suspicious_text_tokens, tuple) \
        or any(not isinstance(token, tuple) for token in original_text_tokens + suspicious_text_tokens)
    ):
        return -1.0

    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_list = list(original_text_tokens)
        for _ in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_list.append("")

        original_text_tokens = tuple(original_list)

    plagiarism_sum = []

    for tokens_index, tokens in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[tokens_index], tokens, plagiarism_threshold)
        plagiarism_sum.append(calculate_plagiarism_score(lcs_length, tokens))

    return sum(plagiarism_sum) / len(plagiarism_sum)

def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    if (
        not isinstance(original_sentence_tokens, tuple) \
        or not isinstance(suspicious_sentence_tokens, tuple) \
        or not isinstance(lcs, tuple) \
        or any(not item for item in original_sentence_tokens + suspicious_sentence_tokens + lcs)
    ):
        return ()

    if not original_sentence_tokens or not suspicious_sentence_tokens:
        return ((), ())

    to_compare = original_sentence_tokens, suspicious_sentence_tokens

    difference_list = []
    for comparing in to_compare:
        difference = []

        for index, token in enumerate(comparing):
            if token not in lcs:
                if not index or comparing[index - 1] in lcs:
                    difference.append(index)
                if index == len(comparing) - 1 or comparing[index + 1] in lcs:
                    difference.append(index + 1)

        difference_list.append(tuple(difference))

    return tuple(difference_list)

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
    original, suspicious = original_text_tokens, suspicious_text_tokens

    diff_stats = {
        "text_plagiarism": calculate_text_plagiarism_score(original, suspicious),
        "sentence_plagiarism": [],
        "sentence_lcs_length": [],
        "difference_indexes": []
    }

    for first_sentence, second_sentence in zip(original, suspicious):
        lcs_length = find_lcs_length(first_sentence, second_sentence, plagiarism_threshold)
        lcs_matrix = fill_lcs_matrix(first_sentence, second_sentence)
        lcs = find_lcs(first_sentence, second_sentence, lcs_matrix)

        diff_stats["sentence_plagiarism"].append(calculate_plagiarism_score(lcs_length, second_sentence))
        diff_stats["sentence_lcs_length"].append(find_lcs_length(first_sentence, second_sentence, plagiarism_threshold))
        diff_stats["difference_indexes"].append(find_diff_in_sentence(first_sentence, second_sentence, lcs))

    return diff_stats

def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    if (
        not isinstance(original_text_tokens, tuple) \
        or not isinstance(suspicious_text_tokens, tuple) \
        or not isinstance(accumulated_diff_stats, dict)
    ):
        return ""
    
    original, suspicious = original_text_tokens, suspicious_text_tokens
    text_length = len(original)
    report = ''
    
    for sentence_index in range(text_length):
        original_sentence = list(original[sentence_index])
        suspicious_sentence = list(suspicious[sentence_index])
        difference_indexes = accumulated_diff_stats["difference_indexes"][sentence_index]
        
        current_insertion = 0
        for difference_index in difference_indexes[0]:
            original_sentence.insert(difference_index + current_insertion, '|')
            suspicious_sentence.insert(difference_index + current_insertion, '|')            
            current_insertion += 1

        original_sentence = ' '.join(original_sentence)
        suspicious_sentence = ' '.join(suspicious_sentence)

        lcs_length = accumulated_diff_stats["sentence_lcs_length"][sentence_index]
        plagiarism = accumulated_diff_stats["sentence_plagiarism"][sentence_index]

        report += """- {}
        + {}

        lcs = {}, plagiarism = {}%

        """.format(original_sentence, suspicious_sentence, lcs_length, plagiarism * 100)

    report += "Text average plagiarism (words): {}%".format(accumulated_diff_stats["text_plagiarism"] * 100)

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
