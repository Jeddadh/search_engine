from collections import OrderedDict
from indexation.saver import save_new_term_termid,save_new_termid_posting
class Index():
    def __init__(self, term_termid, term_termid_path, doc_docid_path, termid_postings_path):
        self.docid_doc = {}
        self.term_termid = term_termid
        self.new_term_termid = {}
        self.termid_postings = {}
        self.set_of_termid_docid = []
        self.term_termid_path = term_termid_path
        self.doc_docid_path = doc_docid_path
        self.termid_postings_path = termid_postings_path

    def add_doc(self, doc_id: int, doc_content: list):
        """
        doc = {doc_id: doc_content}
        doc_content = list_of_words = ["w1","w2",...]
        """
        for word in doc_content :
            term_id = self.term_termid[word] = self.term_termid.get(word,len(self.term_termid))
            self.new_term_termid[word] = self.term_termid[word]
            self.set_of_termid_docid.append((term_id, doc_id))
        return None

    def add_list_of_docs(self, list_of_docs : dict):
        for doc_id in list_of_docs :
            doc_content = list_of_docs[doc_id]
            self.add_doc(doc_id, doc_content)
        return None

    def sort_termid_docid(self):
        self.set_of_termid_docid = sorted(self.set_of_termid_docid)
        return None

    def create_termid_posting(self):
        self.termid_postings = OrderedDict()
        for (term_id, doc_id) in self.set_of_termid_docid :
            self.termid_postings[term_id] = self.termid_postings.get(term_id,OrderedDict())
            self.termid_postings[term_id][doc_id] = self.termid_postings[term_id].get(doc_id,0) + 1

    def apply_BSBI_to_list_of_docs(self, list_of_docs: dict):
        self.add_list_of_docs(list_of_docs)
        self.sort_termid_docid()
        self.create_termid_posting()
        # self.save_index_to_disk(self)

    def save_index_to_disk(self):
        save_new_term_termid(self.term_termid,"cacm", self.term_termid_path,
                        sep = " ",end_car = "\n")
        save_new_termid_posting(self.termid_postings,"cacm", self.term_termid_path)

if __name__=='__main__':
    term_termid = {}
    term_termid_path = "test/result"
    doc_docid_path = "test/result"
    termid_postings_path = "test/result"
    index = Index(term_termid, term_termid_path, doc_docid_path, termid_postings_path)
