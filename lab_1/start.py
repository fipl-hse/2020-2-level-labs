"""
Concordance implementation starter
"""


import os
import main
import time


if __name__ == '__main__':
    def decorator(func):
        def wrapper():
            print('Start running programm')
            start = time.time()
            func()
            end = time.time()
            print('Finish running programm')
            print('[*] Running time: {} secunds.'.format(end-start))
        return wrapper
    
    @decorator
    def made_concordance():
        #  here goes your logic: calling methods from concordance.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
        stop_words = []
        
        #  use data.txt file to test your program
        tokens = main.tokenize(data)
        print('tokenize', tokens[:5])
            
        tokens = main.remove_stop_words(tokens, stop_words)
        print('remove_stop_words', tokens[:5])
            
        frequencies = main.calculate_frequencies(tokens)
        print('calculate_frequencies', frequencies[tokens[0]])
            
        concordance = main.get_concordance(tokens, 'dog', 2, 0)
        print('get_concordance', concordance[:5])
            
        adjacent = main.get_adjacent_words(tokens, 'dog', 2, 0)
        print('get_adjacent_words', adjacent[:5])
            
        sorted_concordance = main.sort_concordance(tokens, 'dog', 2, 0, True)
        print('sort_concordance', sorted_concordance[:5])
            
        main.write_to_file('', sorted_concordance)
        check = (all(isinstance(s, list) for s in sorted_concordance))
        RESULT = isinstance(sorted_concordance, list) and check
        #  DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
        assert RESULT, 'Concordance not working'
    
    made_concordance()
