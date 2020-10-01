"""
Concordance implementation starter
"""

import os
import main
if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt')).split('\n')

    #  here goes your logic: calling methods from concordance.py

    tokens = main.remove_stop_words(main.tokenize(data), stop_words)
    print('tokens without stop words:', tokens[:15])

    frequencies = main.calculate_frequencies(tokens)
    print('frequency for the first word:', frequencies[tokens[0]])

    top_5_words = main.get_top_n_words(frequencies, 5)
    print('top 5 words:', top_5_words)

    concordance = main.get_concordance(tokens, 'street', 2, 3)
    print('concordance for the word "street":', concordance[:5])

    adjacent_words = main.get_adjacent_words(tokens, 'street', 2, 3)
    print('adjacent words for the word "street":', adjacent_words[:5])

    sorted_concordance = main.sort_concordance(tokens, 'street', 2, 3, False)
    print('sorted concordance for the word "street":', sorted_concordance)

    main.write_to_file('report.txt', sorted_concordance)

    RESULT = sorted_concordance[:5]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['originally', 'each', 'street', 'a', 'small', 'siren'],
                      ['located', 'monnow', 'street', 'access', 'clean', 'water'],
                      ['involvement', 'sesame', 'street', 'continued', 'henson', 'mused'],
                      ['on', 'the', 'street', 'corners', 'a', 'population'],
                      ['physically', 'assaulted', 'street', 'deane', 'supporters', 'fixed']], \
        'Concordance not working'
