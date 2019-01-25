import re
def preprocess_sentence(sentence: str,stopwords_list = []) -> list :
    sentence = sentence.lower()
    sentence = re.sub("[\"!#$%&’'\t()*+,-./:;<=>?@[\]^_`{|}~\n]", " ", sentence)
    sentence = re.sub(" +"," ",sentence)
    sentence = sentence.strip()
    sentence = tokenize_sentence(sentence)
    return [word for word in sentence if word not in stopwords_list]

def tokenize_sentence(sentence: str) -> list :
    return sentence.split(" ")
