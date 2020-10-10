
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
    tokens = main.tokenize(text)
    print('tokens:', tokens[:10])

    RESULT = None
    tokens = main.remove_stop_words(tokens, stop_words)
    print('tokens without stop words:', tokens[:10])

    frequencies = main.calculate_frequencies(tokens)
    print('frequency for the first word:', frequencies[tokens[0]])

    top_10 = main.get_top_n_words(freq_dict: dict, top_n: int)
    print('top 10 words:', top_10)

    concordance = main.get_concordance(tokens, 'time', 1, 1)

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ['that', 'time', 'he']
