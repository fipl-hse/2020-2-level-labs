"""
Concordance implementation starter
"""
import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = ['was', 'a']

    #  here goes your logic: calling methods from concordance.py

    if __name__ == '__main__':
        #  use data.txt file to test your program
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
        stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))

        #  here goes your logic: calling methods from concordance.py
        tokens = main.tokenize(data)
        print('tokens: ', tokens[:2])

        stop_words = main.remove_stop_words(tokens, stop_words)
        print('without stop words: ', tokens[:2])

        frequencies = main.calculate_frequencies(tokens)
        print('frequencies:', frequencies[tokens[2]])

        top_n = main.get_top_n_words(frequencies, 2)
        print('top words: ', top_n)

        concordance = main.get_concordance(tokens, 'people', 1, 2)
        print('concordance of words: ', concordance[:2])

    RESULT = concordance[:2]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['in', 'people', 'who', 'wereare'], ['many', 'people', 'that', 'death']]