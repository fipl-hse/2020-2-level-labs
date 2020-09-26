"""
Concordance implementation starter
"""

from main import *
"""
Concordance implementation starter
"""

from main import read_from_file
import os


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(data) #токенезирование
    stop_words = get_stop_words()
    #токены без стоп слов
    tokens_clean = remove_stop_words(tokens, stop_words)
    #частоты токенов
    freq_dict = calculate_frequencies(tokens_clean)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'
