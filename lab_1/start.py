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
    tokenized_data = main.tokenize(data)
    clean_data = main.remove_stop_words(tokenized_data, stop_words)

    # Let`s get top 7 words """
    top_7 = main.get_top_n_words(main.calculate_frequencies(clean_data), 7)
    print(top_7)

    # Now let`s finally get a concordance for word 'people' """
    concordance = main.get_concordance(clean_data, 'people', 3, 1)
    print(concordance[:5])

    # Let`s see 1st on the left and 2nd on the right words around our target word """
    closest_words = main.get_adjacent_words(clean_data, 'people', 1, 2)
    print(closest_words[:5])

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'
