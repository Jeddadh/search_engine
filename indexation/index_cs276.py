from collections import OrderedDict
from indexation.saver import save_new_term_termid,save_new_termid_posting
from indexation.map_reduce import aggregate_list_of_termid_postings
class IndexCS276():
    def __init__(self, data_path, term_termid_path, docid_doc_path, termid_postings_path):
        self.docid_doc = {}
        self.term_termid = {}
        self.new_term_termid = {}
        self.termid_postings = {}
        self.set_of_termid_docid = []
        self.data_path = data_path
        self.term_termid_path = term_termid_path
        self.docid_doc_path = docid_doc_path
        self.termid_postings_path = termid_postings_path

    def create_save_docid_doc(self, path_to_data):
        doc_id = 0
        f = open(self.docid_doc_path,"w")
        for i in range(10):
            path = self.data_path+"/"+str(i)
            docs = os.listdir(path)
            for doc in docs :
                doc_relative_path = str(i) + "_" + doc
                to_write = str(doc_id) + " " + doc_relative_path + "\n"
                f.write(to_write)
                doc_id += 1
        f.close()

    def update_docid_doc(self):
        f = open(self.docid_doc_path,"r")
        self.docid_doc = {}
        for line in f :
            doc_id,doc = line[:-1].split(" ")
            doc_id = int(doc_id)
            self.docid_doc[doc_id] = self.path_to_data + " "
        f.close()

    def doc_to_list_of_words(self,doc_id):
        doc_path = data_path + self.docid_doc[doc_id]
        list_of_words = []
        with open(doc_path,"r") as f :
            for line in f:
                list_of_words += (line.replace("\n"," ").strip()).split(" ")
        return list_of_words

    def add_doc(self, doc_id):
        """
        """
        doc_content = self.doc_to_list_of_words(doc_id)
        for word in doc_content :
            term_id = self.term_termid[word] = self.term_termid.get(word,len(self.term_termid))
            self.new_term_termid[word] = self.term_termid[word]
            self.set_of_termid_docid.append((term_id, doc_id))
        return None

    def add_list_of_docs(self, list_of_doc_ids : list):
        self.set_of_termid_docid = []
        for doc_id in list_of_doc_ids :
            self.add_doc(doc_id)
        return None

    def sort_termid_docid(self):
        self.set_of_termid_docid = sorted(self.set_of_termid_docid)
        return None

    def create_termid_posting(self):
        self.termid_postings = OrderedDict()
        for (term_id, doc_id) in self.set_of_termid_docid :
            self.termid_postings[term_id] = self.termid_postings.get(term_id,OrderedDict())
            self.termid_postings[term_id][doc_id] = self.termid_postings[term_id].get(doc_id,0) + 1

    def create_index(self, max_nb_docs):
        self.update_docid_doc()
        i = 0
        doc_lists = []
        list_of_postings_names = []
        for doc_id in self.docid_doc :
            i += 1
            if i% max_nb_docs == 0 :
                self.add_list_of_docs(doc_lists)
                self.sort_termid_docid()
                self.create_termid_posting()
                postings_name = str(i)+"_1.txt"
                save_new_termid_posting(self.termid_postings, "cs276", self.termid_postings_path,postings_name)
                list_of_postings_names.append(self.termid_postings_path + '/' + postings_name)
                doc_lists = []
        aggregate_list_of_termid_postings(list_of_postings_names)

if __name__=='__main__':
    pass
