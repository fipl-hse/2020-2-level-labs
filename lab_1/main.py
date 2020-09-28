"""
Lab 1
A concordance extraction
"""


import os


def tokenize(text: str) -> list:
    if not isinstance(text, str):
        output = []
    else:
        #  table = str.maketrans({p: None for p in string.punctuation})
        #  output = text.translate(table)
        output = ''.join([char for char in text.lower()
            if char.isalnum() or char.isspace()]).split()
    return output


def remove_stop_words(tokens: list, stop_words: list) -> list:
    if not isinstance(tokens, list):
        output = []
    elif not isinstance(stop_words, list):
        output = tokens
    else:
        output = [word for word in tokens if word not in stop_words]
    return output


def calculate_frequencies(tokens: list) -> dict:
    check = isinstance(tokens, list) or len(tokens) > 0
    if not check or isinstance(tokens[0], str):
        output = {}
    else:
        freqs = {}
        for word in set(tokens):
            freqs[word] = tokens.count(word)
        output = dict(sorted(freqs.items(), key=lambda x: x[1], reverse=True))
    return output


def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        output = []
    else:
        output = sorted(freq_dict, key=freq_dict.get,
            reverse=True)[:top_n]
    return output


def get_concordance(tokens: list,
                    word: str,
                    left_context_size: int,
                    right_context_size: int) -> list:
    if not isinstance(tokens, list) or word not in tokens:
        output = []
    else:
        lcs = left_context_size
        check_l = (not isinstance(lcs, bool)
            and isinstance(lcs, int) and lcs > 0)

        rcs = right_context_size
        check_r = (not isinstance(rcs, bool)
            and isinstance(rcs, int) and rcs > 0)

        idx = [i for i, x in enumerate(tokens) if x == word]

        if check_l and check_r:
            output = [tokens[i-lcs:i+rcs+1] for i in idx]

        elif not check_l and check_r:
            output = [tokens[i:i+rcs+1] for i in idx]

        elif check_l and not check_r:
            output = [tokens[i-lcs:i+1] for i in idx]
    return output


def get_adjacent_words(tokens: list,
                       word: str,
                       left_n: int,
                       right_n: int) -> list:
    if not left_n and not right_n:
        output = []
    elif not left_n:
        conc = get_concordance(tokens, word, left_n, right_n)
        output = [[elem[-1]] for elem in conc]
    elif not right_n:
        conc = get_concordance(tokens, word, left_n, right_n)
        output = [[elem[0]] for elem in conc]
    else:
        conc = get_concordance(tokens, word, left_n, right_n)
        output = [[elem[0], elem[-1]] for elem in conc]
    return output


def read_from_file(path_to_file: str) -> str:
    with open(path_to_file, 'r', encoding='utf-8') as file:
        data = file.read()
    return data


def write_to_file(path_to_file: str, content: list):
    with open(os.path.join(path_to_file, 'report.txt'),
              'w', encoding='utf-8') as file:
        file.write('\n'.join([' '.join(k) for k in content]))


def sort_concordance(tokens: list,
                     word: str,
                     left_context_size: int,
                     right_context_size: int,
                     left_sort: bool) -> list:
    lcs = left_context_size
    rcs = right_context_size

    # validate inputs
    if (not isinstance(left_sort, bool) or
        not (isinstance(lcs, int) or isinstance(rcs, int))):
        output = []
    # logic starts here
    else:
        conc = get_concordance(tokens, word, lcs, rcs)  # list of lists of strs
        if left_sort and lcs > 0:
            output = sorted(conc)
        elif not left_sort and rcs > 0:
            output = sorted(conc, key=lambda x: x[tokens.index(word) + 1])
    return output
