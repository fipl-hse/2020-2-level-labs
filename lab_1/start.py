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
        print('tokens: ', tokens[:3])

        stop_words = main.remove_stop_words(tokens, stop_words)
        print('without stop words: ', tokens[:5])

        frequencies = main.calculate_frequencies(tokens)
        print('frequency for a word:', frequencies[tokens[5]])

        top_n = main.get_top_n_words(frequencies, 10)
        print('top 10 words: ', top_n)

        concordance = main.get_concordance(tokens, 'people', 2, 3)
        print('concordance for the word: ', concordance[:5])

    RESULT = concordance[:5]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['presented', 'in', 'people', 'who', 'wereare', 'not'], ['persuaded', 'many', 'people', 'that', 'death', 'was'], ['among', 'these', 'people', 'and', 'had', 'buried'], ['distancesafrican', 'creole', 'people', 'in', 'the', 'early'], ['airplaneafter', 'the', 'people', 'are', 'happily', 'fed']], 'Concordance not working'
