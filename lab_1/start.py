from main import read_from_file
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import get_concordance
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file((os.path.join(current_dir, 'stop_words.txt')))
    stop_words = stop_words.split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(text)[:101]
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    top_words = get_top_n_words(freq_dict, 3)

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ['that', 'time', 'he']
