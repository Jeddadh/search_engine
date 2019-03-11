from data_creation import get_cacm_data_as_dict,preprocessing_and_vocabulary_creation
from global_variables import path_cacm_all
import numpy as np
from collections import OrderedDict
import matplotlib.pyplot as plt

def get_nb_of_tokens(preprocessed_collection:dict, *text_keys)-> int :
    nb_tokens = 0
    for doc_id in preprocessed_collection :
        for key in text_keys :
            try :
                nb_tokens += len(preprocessed_collection[doc_id][key])
            except KeyError :
                continue

    return nb_tokens

def get_vocab_size(collection_vocabulary_key:dict, *text_keys:str) -> (set,int):
    all_vocab = set()
    for key in text_keys :
        all_vocab = all_vocab.union(collection_vocabulary_key[key])
    return all_vocab, len(all_vocab)

def get_nbtoknes_vocab_size_halfcollection(preprocessed_collection:dict, *text_keys) -> (int,int) :
    n = len(preprocessed_collection)
    i = 0
    nb_tokens = 0
    vocab = set()
    for doc_id in preprocessed_collection :
        for key in text_keys :
            try :
                nb_tokens += len(preprocessed_collection[doc_id][key])
                vocab = vocab.union(set(preprocessed_collection[doc_id][key]))
            except KeyError:
                continue
        i += 1
        if i >= n/2 :
            break
    vocab_size = len(vocab)
    return vocab_size, nb_tokens


def get_heap_params(all_vocab_size, all_nbtokens,half_vocab_size, half_nbtokens):
    b =(np.log(all_vocab_size) - np.log(half_vocab_size)) /(np.log(all_nbtokens) - np.log(half_nbtokens))
    k = np.exp(np.log(all_vocab_size) - b*np.log(all_nbtokens))
    return b,k

def get_word_frequency_and_rank(preprocessed_collection:dict,*text_keys):
    vocab = {}
    for doc_id in preprocessed_collection :
        for key in text_keys :
            try :
                for word in preprocessed_collection[doc_id][key] :
                    vocab[word] = vocab.get(word,0) + 1
            except KeyError :
                continue
    ordred_vocab = OrderedDict(sorted(vocab.items(), key=lambda t: t[1],reverse = True))
    return ordred_vocab

def plot_freq_vs_rank(ordred_vocab, data_name = ""):
    n = len(ordred_vocab)
    x = np.arange(1,n+1)
    y = np.array(list(ordred_vocab.values()))
    plt.figure()
    plt.plot(x, y)
    plt.title("freq vs rank {data_name}".format(data_name=data_name))
    plt.xlabel("rank")
    plt.ylabel("freq")

def plot_freq_vs_rank_log(ordred_vocab, data_name = ""):
    n = len(ordred_vocab)
    x = np.arange(1,n+1)
    x = np.log10(x)
    y = np.array(list(ordred_vocab.values()))
    y = np.log10(y)
    plt.figure()
    plt.plot(x, y)
    plt.title("freq vs rank {data_name}".format(data_name=data_name))
    plt.xlabel("rank")
    plt.ylabel("freq")

if __name__ == "__main__" :
    cacm_dict = get_cacm_data_as_dict(path_cacm_all)
    preprocessed_collection, collection_vocabulary_key, vocab_by_doc_key = preprocessing_and_vocabulary_creation(cacm_dict, "abstract", "title","key_words")
    all_vocab_size = get_vocab_size(collection_vocabulary_key,"title","abstract","key_words")[1]
    all_nbtokens =  get_nb_of_tokens(preprocessed_collection,"title","abstract","key_words")
    print("vocabulary size : " ,all_vocab_size)
    print("number of tokens : " , all_nbtokens)
    half_vocab_size, half_nbtokens =  get_nbtoknes_vocab_size_halfcollection(preprocessed_collection,"title","abstract","key_words")
    b,k = get_heap_params(all_vocab_size, all_nbtokens,half_vocab_size, half_nbtokens)
    print("b = {b}, k = {k}".format(b=b,k=k))
    frequency_dic = get_word_frequency_and_rank(preprocessed_collection,"title","abstract","key_words")
    # print(frequency_dic)
    plot_freq_vs_rank(frequency_dic)
    plot_freq_vs_rank_log(frequency_dic)
    plt.show()
