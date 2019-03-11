

if __name__ == "__main__" :
    # from global_variables import path_cacm_all,path_cacm_common_words
    # from indexation.index import Index
    # from data_creation import get_cacm_data_as_dict,preprocessing_and_vocabulary_creation
    # from indexation.saver import get_termid_posting
    # cacm_dict = preprocessing_and_vocabulary_creation(get_cacm_data_as_dict(path_cacm_all))
    # term_termid = {}
    # term_termid_path = "indexation/test/result/cacm"
    # doc_docid_path = "indexation/test/result/cacm"
    # termid_postings_path = "indexation/test/result/cacm"
    # index = Index(term_termid, term_termid_path, doc_docid_path, termid_postings_path)
    # index.apply_BSBI_to_list_of_docs(cacm_dict)
    # # print(index.set_of_termid_docid)
    # # print(index.term_termid)
    # index.save_index_to_disk()
    # termid_posting = get_termid_posting(termid_postings_path+"/termid_postings.txt")
    # print(termid_posting)
    from models.boolean import BooleanModel
    path_to_index, collection_name = "indexation/test/result", "cacm"
    query = "procedures "
    bool_model = BooleanModel(path_to_index, collection_name)
    print(bool_model.request(query))
