"""
Language detector implementation starter
"""

# import lab_3.main
from lab_3 import main

if __name__ == '__main__':

    # here goes your function calls
    text = 'She is happy. He is happy.'
    tokens = main.tokenize_by_sentence(text)
    print(tokens)

    let_storage = main.LetterStorage()
    let_storage.update(tokens)
    print(let_storage.storage)

    encoded_corpus = main.encode_corpus(let_storage, tokens)
    print(encoded_corpus)

    n_gram = main.NGramTrie(2)
    extracted_ngrams = n_gram.fill_n_grams(encoded_corpus)
    frequencies = n_gram.calculate_n_grams_frequencies()
    top = n_gram.top_n_grams(2)
    print('Frequencies: ', frequencies)
    print('Top 2: ', top)



    RESULT = top
    #DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((1, 3), (3, 4)), 'Not working'
