"""
Text generator implementation starter
"""

from lab_4.main import tokenize_by_sentence, WordStorage, encode_text, LikelihoodBasedTextGenerator, decode_text
from lab_4.ngrams.ngram_trie import NGramTrie


if __name__ == '__main__':

    raw_text = '''You sit here, dear. All right. Morning! Morning! Well, what have you got? Well, there is egg and
    bacon; egg sausage and bacon; egg and spam; egg bacon and spam; egg bacon sausage and spam; spam bacon sausage and
    spam; spam egg spam bacon and spam; spam sausage spam bacon spam tomato and spam; spam egg and spam; spam baked
    beans spam... Spam! Lovely spam! Lovely spam! ...or Lobster Thermidor au Crevette with a Mornay sauce served in a
    Provencale manner with shallots and aubergines garnished with truffle pate, brandy and with a fried egg on top and
    spam. Have you got anything without spam? Well, there's spam egg sausage and spam, that's not got much spam in it.
    I do not want ANY spam! Why cannot she have egg bacon spam and sausage? THAT'S got spam in it! Has not got as much
    spam in it as spam egg sausage and spam, has it? Could you do the egg bacon spam and sausage without the spam then?
    Urgghh! What do you mean 'Urgghh'? I do not like spam! Lovely spam! Wonderful spam! Shut up! Bloody Vikings! You
    cannot have egg bacon spam and sausage without the spam. I do not like spam! Sshh, dear, do not cause a fuss.
    I will have your spam. I love it. I am having spam beaked beans spam and spam! Lovely spam! Wonderful spam! 
    Shut up! Baked beans are off. Well could I have her spam instead of the baked beans then?'''

    corpus = tokenize_by_sentence(raw_text)

    storage = WordStorage()
    storage.update(corpus)

    encoded_text = encode_text(storage, corpus)

    n_gram_trie = NGramTrie(3, encoded_text)

    generator = LikelihoodBasedTextGenerator(storage, n_gram_trie)

    context = (storage.get_id('bloody'), storage.get_id('vikings'))
    generated_text = generator.generate_text(context, 5)

    decoded_text = decode_text(storage, generated_text)

    IS_WORKING = True
    for sentence in decoded_text:
        if '<END>' in sentence or not sentence[0].isupper() or not sentence[-1].isalpha():
            IS_WORKING = False

    print(decoded_text)

    RESULT = IS_WORKING
    assert RESULT, 'Not working'
