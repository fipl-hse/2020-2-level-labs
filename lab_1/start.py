"""
Concordance implementation starter
"""
import os
import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    #  here goes your logic: calling methods from concordance.py

    tokens = main.tokenize(data)
    print("tokens:", tokens[:15])

    tokens_stop_words = main.remove_stop_words(tokens, stop_words)
    print("tokens without stop words:", tokens_stop_words[:7])

    frequencies = main.calculate_frequencies(tokens)
    print('frequencies for the word: ', frequencies[tokens[2]])

    top_words = main.get_top_n_words(frequencies, 5)
    print("top words:", top_words)

    concordance = main.get_concordance(tokens, 'time', 1, 3)
    print(" concordance:", concordance[:3])

    RESULT = adjacent_words[:3]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['presented', 'wereare'], ['persuaded', 'death'], ['among', 'had']], 'Concordance not working'
