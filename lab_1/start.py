"""
Concordance implementation starter
"""

import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = ['of', 'a']

    #  here goes your logic: calling methods from concordance.py

    tokens = main.tokenize(data)
    print(f'TOKENIZE >> {tokens[:10]}')

    tokens = main.remove_stop_words(tokens, stop_words)
    print(f'REMOVE STOPWORDS >> {tokens[:10]}')

    freqs = main.calculate_frequencies(tokens[:5000])
    print(f'CALCULATE FREQUENCIES >> {freqs[tokens[2]]} TIMES')

    concordance = main.get_concordance(tokens, '195', 2, 3)
    print(f'GET CONCORDANCE >> {concordance[:2]}')

    adjacent_words = main.get_adjacent_words(tokens, '195', 2, 3)
    print(f'GET ADJACENT WORDS >> {adjacent_words[:2]}')

    sorted_concordance = main.sort_concordance(tokens, '195', 2, 3, False)
    print(f'SORT CONCORDANCE >> {sorted_concordance[:2]}')

    main.write_to_file('report.txt', sorted_concordance)
    print('WRITE TO FILE >> SUCCESSFUL')

    RESULT = sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['art', 'pp', '195', '216', 'stained', 'glass'],
                      ['existing', 'ones', '195', 'after', 'he', 'became']], 'Concordance not working'
