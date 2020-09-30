"""
Concordance implementation starter
"""

# from main import read_from_file
import os
from lab_1 import main
from lab_1.main import read_from_file

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = ['the', 'is']

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print(tokens[:10])

    tokens = main.remove_stop_words(tokens[:5], stop_words)
    print(tokens)

    freq = main.calculate_frequencies(tokens[:40])
    print(freq[tokens[0]])

    concordance = main.get_concordance(tokens, 'team', 1, 1)
    print(concordance[:2])

    adj_words = main.get_adjacent_words(tokens, 'team', 2, 2)
    print(adj_words[:2])

    # file = main.read_from_file('report.txt', concordance)
    main.write_to_file('report.txt', concordance)

    RESULT = tokens
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ['years', 'of', 'time', 'team', 'presented'],'Concordance not working'
