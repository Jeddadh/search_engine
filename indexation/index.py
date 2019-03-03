
class Index():
    def __init__(self, term_termid, term_termid_path,doc_docid_path, termid_postings_path):
        self.docid_doc = {}
        self.term_termid = term_termid
        self.new_term_termid = {}
        self.termid_postings = {}
        self.set_of_termid_docid = []
        self.term_termid_path = file_path
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
            self.set_of_termid_docid.add((term_id, doc_id))
        return None

    def add_list_of_docs(self, list_of_docs : list):
        for (doc_id, doc_content) in list_of_docs :
            self.add_doc(doc_id, doc_content)
        return None

    def sort_termid_docid(self):
        self.set_of_termid_docid = sorted(self.set_of_termid_docid)
        return None

    def create_termid_posting(self):
        self.termid_postings = {}
        for (term_id, doc_id) in self.set_of_termid_docid :
            self.termid_postings[term_id] = self.termid_postings.get(term_id,[]) + [doc_id]

    def apply_BSBI_to_list_of_docs(self, list_of_docs: list):
        self.add_list_of_docs(list_of_docs)
        self.sort_termid_docid()
        self.create_termid_posting()
        self.save_index_to_disk(self)

    def save_index_to_disk(self):
        raise NotImplementedMethod()
