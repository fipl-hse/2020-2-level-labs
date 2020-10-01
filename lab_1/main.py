"""
Lab 1
A concordance extraction
"""


def tokenize(text: str) -> list:
    k = 0
    for i in range(len(text)):  # проверка строки на корректность
        if 48 <= ord(text[i]) <= 57 or (128 <= ord(text[i]) <= 175 or 224 <= ord(text[i]) <= 243):
            k += 1
            break

    if k != 0:  # если некорректные токены
        return []
    else:
        string = text.lower()  # понизили регистр букв (сделали все строчными)
        signs = ",;:\"\'.!?—()-><|"
        for i in range(len(text)):  # цикл по длине строки
            for j in range(len(signs)):  # цикл по длине строки с количеством знаков
                if string[i] == signs[j]:  # если в введенной строке нашли знак препинания
                    string = string[:i] + ' ' + string[i + 1:]  # строка до знака препинания, пробел и строка после знака
        return string.split()


def remove_stop_words(tokens: list, stop_words: list) -> list:
    k = 0
    for i in range(len(tokens)):  # проверка строки на корректность
        if 48 <= ord(' '.join(tokens)[i]) <= 57 or (128 <= ord(' '.join(tokens)[i]) <= 175 or 224 <= ord(' '.join(tokens)[i]) <= 243):
            k += 1
            break
    m = 0
    for i in range(len(stop_words)):  # проверка стоп-слов на корректность
        if 48 <= ord(stop_words[i]) <= 57 or (128 <= ord(stop_words[i]) <= 175 or 224 <= ord(stop_words[i]) <= 243):
            m += 1
            break
    if k != 0:  # если некорректные токены
        return []
    elif m != 0:  # если корректные токены, но некорректные стоп-слова, то возвращаем список токенов без изменений
        tokenize(string)

    else:  # если всё корректно
        stop_words = stop_words.split()
        tokens = [token for token in tokens if token not in stop_words]
        return tokens

def calculate_frequencies(tokens: list) -> dict:
    k = 0
    for i in range(len(tokens)):  # проверка строки на корректность
        if 48 <= ord(' '.join(tokens)[i]) <= 57 or (128 <= ord(' '.join(tokens)[i]) <= 175 or 224 <= ord(' '.join(tokens)[i]) <= 243):
            k += 1
            break

    if k != 0:  # если некорректные токены
        return []
    else:
        dictionary = {}
        for elem in tokens:
            if elem in dictionary:
                dictionary[elem] += 1
            else:
                dictionary[elem] = 1
        return dictionary


def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    k = 0
    for i in range(len(string)):  # проверка строки на корректность
        if 48 <= ord(' '.join(string)[i]) <= 57 or (128 <= ord(' '.join(string)[i]) <= 175 or 224 <= ord(' '.join(string)[i]) <= 243):
            k += 1
            break

    if k != 0:  # если некорректные токены
        return []
    else:
        top_n = []
        frequency = []
        number = 0
        for key, value in dictionary.items():
            frequency.append([value, key])
        frequency.sort(reverse=True)
        if n <= len(frequency):
            for element in frequency:
                if number < n:
                    top_n.append(element[1])
                    number += 1
            return top_n



def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int) -> list:
    k = 0
    for i in range(len(tokens)):  # проверка строки на корректность
        if 48 <= ord(' '.join(tokens)[i]) <= 57 or (128 <= ord(' '.join(tokens)[i]) <= 175 or 224 <= ord(' '.join(tokens)[i]) <= 243):
            k += 1
            break
    m = 0
    for i in range(len(word)):  # проверка слова на корректность
        if 48 <= ord(word[i]) <= 57 or (128 <= ord(word[i]) <= 175 or 224 <= ord(word[i]) <= 243):
            m += 1
            break

    concordance = []
    if k != 0 or m != 0 or (left_context_size == 0 and right_context_size == 0) or (i - left_context_size < 0 and i + 1 + right_context_size > len(string) - 1):  # если некорректные токены
        return []
    else:
        for i in range(len(tokens)):
            if word == tokens[i]:
                if i - left_context_size > 0 and i + 1 + right_context_size < len(tokens) - 1:
                    concordance.append(tokens[i - left_context_size:i + 1 + right_context_size])
                elif i - left_context_size < 0:
                    concordance.append(tokens[i:i + 1 + right_context_size])
                elif i + 1 + right_context_size > len(tokens) - 1:
                    concordance.append(tokens[i - left_context_size:i + 1])
    return concordance

def get_adjacent_words(tokens: list, word: str, left_n: int, right_n: int) -> list:
    global i
    k = 0
    for i in range(len(tokens)):  # проверка строки на корректность
        if 48 <= ord(' '.join(tokens)[i]) <= 57 or (128 <= ord(' '.join(tokens)[i]) <= 175 or 224 <= ord(' '.join(tokens)[i]) <= 243):
            k += 1
            break
    m = 0
    for i in range(len(word)):  # проверка слова на корректность
        if 48 <= ord(word[i]) <= 57 or (128 <= ord(word[i]) <= 175 or 224 <= ord(word[i]) <= 243):
            m += 1
            break

    adjacent_words = []
    if k != 0 or m != 0 or (left_n == 0 and right_n == 0) or (i - left_n < 0 and i + 1 + right_n > len(tokens) - 1):  # если некорректные токены
        return []
    else:
        for i in range(len(tokens)):
            if word1 == tokens[i]:
                if i - left_n > 0 and i + 1 + right_n < len(tokens) - 1:  # если не выходим за границы
                    adjacent_words.append([tokens[i - left_n], tokens[i + right_n]])
                elif i - left_context_size < 0:
                    adjacent_words.append(tokens[i + right_n])
                elif i + 1 + right_context_size > len(tokens) - 1:
                    adjacent_words.append(tokens[i - left_n])
    return adjacent_words


def read_from_file(path_to_file: str) -> str:
    with open(path_to_file, 'r', encoding = 'utf-8') as report:
        data = report.read()

    return data


def write_to_file(path_to_file: str, content: list):
    with open(path_to_file, 'r') as report:
        for i in range(len(concordance)):
            report.write(' '.join(concordance[i]))
            report.write('\n')

