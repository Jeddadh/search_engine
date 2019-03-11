import re
def preprocess_sentence(sentence: str,stopwords_list = [],lower = True, caracteres = None) -> list :
    if lower :
        sentence = sentence.lower()
    if caracteres is None :
        caracteres = "[\"!#$%&’'\t()*+,-./:;<=>?@[\]^_`{|}~\n0123456789]"
        # print(type(caracteres))
    sentence = re.sub(caracteres, " ", sentence)
    sentence = re.sub(" +"," ",sentence)
    sentence = sentence.strip()
    sentence = tokenize_sentence(sentence)
    return [word for word in sentence if word not in stopwords_list]

def tokenize_sentence(sentence: str) -> list :
    sentence = sentence.split(" ")
    while "" in sentence :
        sentence.remove("")
    return sentence
