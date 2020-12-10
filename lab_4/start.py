'''
Implementation of the text generation
'''

from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import WordStorage, LikelihoodBasedTextGenerator
from lab_4.main import tokenize_by_sentence, encode_text, decode_text


if __name__ == '__main__':

    text = '''
           There are many big and small libraries everywhere in our country. 
           They have millions of books in different languages. 
           You can find there the oldest and the newest books.
           Every school has a library. Pupils come to the library to take books on different subjects.
           The school library where Oleg studies is good. It is a large clean room. 
           There are four big windows in it. The walls are light blue. There are a lot of shelves full of books. 
           You can find books on literature, physics, history, chemistry, geography, biology and other subjects. 
           There are books in English, too. On the walls you can see pictures of some great writers and poets.
           On the table near the window you can always see beautiful spring and autumn flowers.
           Oleg likes to go to the library. He can always find there something new, something he needs.
           '''
    corpus = tokenize_by_sentence(text)
    print(f'TOKENIZE_BY_SENTENCE RESULT: {corpus}\n')

    word_storage = WordStorage()
    word_storage.update(corpus)
    encoded_text = encode_text(word_storage, corpus)
    print(f'ENCODE_TEXT RESULT: {encoded_text}\n')

    trie = NGramTrie(4, encoded_text)
    context = (word_storage.get_id('the'),
               word_storage.get_id('walls'),
               word_storage.get_id('are'))
    likelihood_generator = LikelihoodBasedTextGenerator(word_storage, trie)
    generated_text = likelihood_generator.generate_text(context, 3)
    print(f'ENCODED_GENERATED_TEXT: {generated_text}\n')

    decoded_text = decode_text(word_storage, generated_text)
    print(f'DECODED_GENERATED_TEXT: {decoded_text}')


    RESULT = decoded_text
    assert RESULT == ('The walls are light blue',
                      'There are books in english too',
                      'On the walls you can see pictures of some great writers and poets'), 'Generator not working'



