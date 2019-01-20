import re

def preprocess_sentence(sentence: str) -> list :
    sentence = sentence.lower()
    sentence = re.sub("[\"!#$%&’'\t()*+,-./:;<=>?@[\]^_`{|}~\n]", " ", sentence)
    sentence = re.sub(" +"," ",sentence)
    sentence = sentence.strip()
    sentence = tokenize_sentence(sentence)
    return sentence

def tokenize_sentence(sentence: str) -> list :
    return sentence.split(" ")
