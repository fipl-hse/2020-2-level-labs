
import main
from main import read_from_file
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file((os.path.join(current_dir, 'stop_words.txt')))
    stop_words = stop_words.split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(text)
    print("tokens:", tokens[:15])
    RESULT = tokens
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT
