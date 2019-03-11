from global_variables import path_cacm_all,path_cacm_common_words
from preprocessing import preprocess_sentence
import re

def get_key_words(key_words: str) -> list:
    # list_of_key_words = re.split("[ ,]",key_words)
    list_of_key_words = preprocess_sentence(key_words)
    while "" in list_of_key_words :
        list_of_key_words.remove("")
    return [key_word.strip() for key_word in list_of_key_words]

def get_cacm_data_as_dict(file_name: str, merge = True) -> dict:
    """
    returns a dict corresponding to data :
    if merge is True
        {doc_id : [list of words]}
    if merge is False
        {doc_id : [list of words]}
    """
    with open(file_name,"r") as f :
        documents = {}
        header = ""
        doc_id = None
        meaning = {"W":"abstract","T":"title","K":"key_words"}
        while(True):
            try:
                line = next(f)
                if len(line) >= 2 :
                    match = re.match(".[ITWBXNKAC]",line[:2])
                    if match is None and doc_id is not None:
                        if header == None or header == "I" :
                            continue
                        documents[doc_id][meaning[header]] = documents[doc_id].get(meaning[header],"") + line
                    else :
                        if not re.match(".[ITWK]",match.group(0)):
                            header = None
                        elif match.group(0) == ".I" :
                            doc_id = line[3:]
                            doc_id = doc_id.replace("\n","")
                            doc_id = int(doc_id)
                            documents[doc_id] = {}
                            header = "I"
                        else :
                            header =  match.group(0)[1]
                elif doc_id is not None:
                    if header == None or header == "I" :
                        continue
                    documents[doc_id][meaning[header]] = documents[doc_id].get(meaning[header],"") + line

            except StopIteration :
                break
        for doc_id in documents :
            if not merge :
                documents[doc_id]["key_words"] = get_key_words(documents[doc_id].get("key_words",""))
            if merge :
                documents[doc_id] = documents[doc_id].get("key_words",'') + " " + \
                                    documents[doc_id].get("title",'') + " " + \
                                    documents[doc_id].get("abstract",'')
    return documents

def get_stopwords_list(file_name:str) -> list :
    stopwords_list = []
    with open(file_name,"r") as f :
        while(True):
            try :
                line = next(f)
                line = line.replace('\n',"").lower().strip()
                stopwords_list.append(line)
            except StopIteration :
                break
    return stopwords_list

def preprocessing_and_vocabulary_creation(collection_dict: dict,merge = True, *text_keys ) -> (dict,dict,dict) :
    preprocessed_collection = {}
    if merge :
        for doc_id in collection_dict:
            preprocessed_collection[doc_id] = preprocess_sentence(collection_dict[doc_id])
            if "" in preprocessed_collection[doc_id] :
                print(preprocessed_collection[doc_id])
        return preprocessed_collection
    collection_vocabulary_key = {key :set() for key in text_keys}
    vocab_by_doc_key = {}
    for doc_id in collection_dict :
        preprocessed_collection[doc_id] = collection_dict[doc_id].copy()
        vocab_by_doc_key[doc_id] = {key :set() for key in text_keys}
        for key in text_keys :
            try :
                preprocessed_collection[doc_id][key] = preprocess_sentence(preprocessed_collection[doc_id][key])
            except KeyError:
                continue
            except AttributeError :
                preprocessed_collection[doc_id][key] = preprocessed_collection[doc_id][key]
            except TypeError :
                preprocessed_collection[doc_id][key] = preprocessed_collection[doc_id][key]

            for word in preprocessed_collection[doc_id][key] :
                collection_vocabulary_key[key].add(word)
                vocab_by_doc_key[doc_id][key].add(word)

    return preprocessed_collection, collection_vocabulary_key, vocab_by_doc_key

if __name__ == "__main__" :
    cacm_dict = get_cacm_data_as_dict(path_cacm_all)
    print(cacm_dict)
    # preprocessed_collection, collection_vocabulary_key, vocab_by_doc_key = preprocessing_and_vocabulary_creation(cacm_dict, "abstract", "title","key_words")
    # print(collection_vocabulary_key)
