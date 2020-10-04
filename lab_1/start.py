"""
Concordance implementation starter
"""

from main import read_from_file
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import get_concordance
from main import get_adjacent_words
import os

if __name__ == '__main__':
    # use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split()
    
    string = tokenize(data)[:10]
    print("tokenize: ", string)
    
    string_new = remove_stop_words(string, stop_words)
    print("remove_stop_words: ", string_new)

    dictionary = calculate_frequencies(string_new)
    print("calculate_frequencies: ", dictionary)
    
    top_n = get_top_n_words(dictionary, 3)
    print("get_top_n_words: ", top_n)

    concordance = get_concordance(string_new, 'presented', 3, 1)
    print("get_concordance: ", concordance)    

    adjacent_words = get_adjacent_words(string, 'presented', 2, 1)
    print("get_adjacent_words: ", adjacent_words) 

#    write_to_file(r"D:\Прога\Python\report.txt", concordance)

    #  here goes your logic: calling methods from concordance.py

    RESULT = None
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'
