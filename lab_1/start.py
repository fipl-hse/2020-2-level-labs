"""
Concordance implementation starter
"""

from main import read_from_file, sort_concordance
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
tokens = read_from_file('data.txt')
    RESULT = sort_concordance(tokens, 'text', 1, 2, True)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['80', 'text', 'columns', 'although'], ['and', 'text', 'messaging', 'mobile'], ['arabic', 'text', 'have', 'been'], ['and', 'text', 'dolkart', 'andrew'], ['a', 'text', 'as', 'quickly'], ['a', 'text', 'or', 'laboratory'], ['actual', 'text', 'the', 'information'], ['biblical', 'text', '5016', 'mid-sized'], ['displaying', 'text', 'within', 'graphics'], ['essence', 'text', 'requiring', 'an'], ['full', 'text', 'of', 'the'], ['final', 'text', '7719', 'the'], ['five-minute', 'text', 'chat', '8444'], ['gnostic', 'text', 'the', 'apocryphal'], ['his', 'text', '1352', 'by'], ['ia5', 'text', '1858', 'drainage'], ['its', 'text', 'differs', 'however'], ['incorporates', 'text', 'from', 'a'], ['latin', 'text', 'in', 'praise'], ['mischmasch', 'text', 'carroll', 'states'], ['monolingual', 'text', 'corpus', '9898'], ['on-screen', 'text', 'to', 'aid'], ['prepare', 'text', 'graphs', 'or'], ['plain', 'text', 'across', 'the'], ['s', 'text', '5278', 'new'], ['the', 'text', 'in', 'these'], ['the', 'text', 'of', 'the'], ['the', 'text', 'of', 'the'], ['this', 'text', 'explains', 'how'], ['the', 'text', 'we', 'are']]