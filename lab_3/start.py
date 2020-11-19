"""
Language detector implementation starter
"""
import main

if __name__ == '__main__':
    text = 'Horse is beautiful. Dog is beautiful.'
    tokens = main.tokenize_by_sentence(text)
    print(tokens)

    storage = main.LetterStorage()
    storage.update(tokens)
    print(storage.storage)

    encoded_corpus = main.encode_corpus(storage, tokens)
    print(encoded_corpus)

    bi_gram = main.NGramTrie(2)
    filles = bi_gram.fill_n_grams(encoded_corpus)
    frequencies = bi_gram.calculate_n_grams_frequencies()
    the_top = bi_gram.top_n_grams(5)
    print('Frequencies: ', frequencies)
    print('Top 5: ', the_top)



    RESULT = the_top
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT,  ((0, 5), (4, 9), (6, 0), (3, 5), (1, 5))
    'Not working'
