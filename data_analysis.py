from data_creation import get_cacm_data_as_dict,preprocessing_and_vocabulary_creation
from global_variables import path_cacm_all
import numpy as np
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
    return vocab_size,nb_tokens

def get_heap_params(all_vocab_size, all_nbtokens,half_vocab_size, half_nbtokens):
    b =(np.log(all_vocab_size) - np.log(half_vocab_size)) /(np.log(all_nbtokens) - np.log(half_nbtokens))
    k = np.exp(np.log(all_vocab_size) - b*np.log(all_nbtokens))
    return b,k

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
