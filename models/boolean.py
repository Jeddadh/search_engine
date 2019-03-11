from indexation.saver import get_term_termid,get_termid_posting
from global_variables import term_termid_file_name, termid_postings_file_name

class Node():
    def __init__(self, left_index, right_index, query, model):
        self.left_index = left_index
        self.right_index = right_index
        self.children = []
        self.parent = None
        self.operation = None
        self.query = query
        self.right_word = None
        self.left_word = None
        self.model = model

    def add_child(self, child):
        child.set_parent(self)
        self.children.append(child)

    def set_parent(self,parent):
        self.parent = parent

    def has_parent(self):
        if self.parent == None :
            return False
        return True

    def is_child_of_couple_index(self, couple_index):
        if self.has_parent():
            return False
        if self.left_index <= couple_index[0] :
            return False
        if self.right_index >= couple_index[1]:
            return False
        return True

    def is_leaf(self):
        return not self.children

    def get_operation(self):
        if self.is_leaf() :
            try :
                op = self.query[self.left_index+1:self.right_index].split(" ")[1]
            except IndexError :
                pass
            self.left_word = self.query[self.left_index+1:self.right_index].split(" ")[0]
            try :
                self.right_word = self.query[self.left_index+1:self.right_index].split(" ")[2]
            except :
                pass
            return op

        if len(self.children) == 1 :
            op = self.query[self.left_index+1:self.right_index].split(" ")[1]
            self.left_word = self.query[self.left_index+1:self.right_index].split(" ")[0]
            return op

        left_child = self.children[0]
        right_child = self.children[1]
        op = self.query[left_child.right_index+1:right_child.left_index].strip().split(" ")[0]
        return op

    def and_operation(self, liste1, liste2):
        return set(liste1).intersection(set(liste2))

    def or_operation(self, liste1, liste2):
        return set(liste1).union(set(liste2))

    def not_operation(self, liste, all_list):
        return set(all_list).difference(set(liste))

    def get_result(self):
        op = self.get_operation()
        if self.is_leaf():
            liste1 = self.model.query_on_word(self.left_word)
            if self.right_word is None :
                return set(liste1)
            liste2 = self.model.query_on_word(self.right_word)
        elif len(self.children) == 1 :
            liste1 = self.model.query_on_word(self.left_word)
            liste2 = self.children[0].get_result()
        else :
            liste1 = self.children[0].get_result()
            liste2 = self.children[1].get_result()

        if op == BooleanModel.AND_operator :
            return self.and_operation(liste1, liste2)
        elif op == BooleanModel.OR_operator :
            return self.or_operation(liste1, liste2)
        elif op == BooleanModel.NOT_operator :
            raise NotIm()


class BooleanModel():
    AND_operator = "&&"
    OR_operator = "||"
    NOT_operator = "!!"
    doc_id_index = 0
    def __init__(self, path_to_index, collection_name):
        self.term_termid = get_term_termid(path_to_index+"/"+collection_name+"/"+term_termid_file_name)
        self.collection_name = collection_name
        if collection_name == "cacm":
            self.termid_postings = get_termid_posting(path_to_index+"/"+collection_name+"/"+termid_postings_file_name)

    def request(self, query:str,data_collection_name :str = "") -> list :
        """
        takes a logic request in the form of (word1 && word2) || (word1 && Word2) && ( !!(wordx) )  ...
        It may be as complex as you want

        returns a list of documents ID
        """
        tree = self.get_tree_from_query(query)
        return tree.get_result()


    # @staticmethod
    def get_tree_from_query(self, query: str, open_parenthese : str = "(",close_parenthese : str = ")"):
        nb_open_parentheses = 0
        open_parenthese_indices = []
        nb_close_parentheses = 0
        close_parenthese_indices = []
        for i,ch in enumerate(query) :
            if ch == open_parenthese :
                nb_open_parentheses += 1
                open_parenthese_indices.append(i)
            elif ch == close_parenthese :
                nb_close_parentheses += 1
                close_parenthese_indices.append(i)
        couple_liste = []
        for cp in close_parenthese_indices :
            i = 0
            while i < len(open_parenthese_indices) and open_parenthese_indices[i] < cp :
                i += 1
            i -= 1
            try :
                open_index = open_parenthese_indices.pop(i)
            except IndexError :
                raise BooleanQueryFormException()
            close_index = cp
            if cp <= open_index :
                raise BooleanQueryFormException()
            couple_liste.append((open_index,close_index))
        liste_of_nodes = []
        for couple_index,couple in enumerate(couple_liste) :
            new_node = Node(*couple,query,self)
            liste_of_nodes.append(new_node)
            for node in liste_of_nodes[:len(liste_of_nodes)]:
                if node.is_child_of_couple_index(couple):
                    print(node.left_index)
                    new_node.add_child(node)
        has_root1 = True
        has_root2 = True
        root = Node(-1,len(query),query,self)
        for node in liste_of_nodes :
            if not node.has_parent():
                if not has_root1 :
                    has_root2 = False
                has_root1 = False
        if has_root2:
            for node in liste_of_nodes:
                if node.left_index  == 0:
                    return node
        return root

    # def get_liste_of_words_postings(self, collection: str, list_of_words: list):
    #     if collection == "cacm" :
    #         pass

    def query_on_word(self,word):
        if self.collection_name == "cacm":
            term_id = self.term_termid.get(word,None)
            docs = self.termid_postings.get(term_id,[])
            return docs


if __name__ == "__main__" :
    query = "a && (b || (c && d))"
    tree  = BooleanModel.get_tree_from_query(query)
