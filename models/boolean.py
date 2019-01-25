# from indexation.inversed_index import *

class BooleanModel():
    doc_id_index = 0
    def __init__(self,):
        pass

    def request(query:str,data_collection_name :str = "") -> list :
        """
        takes a logic request in the form of (word1 && word2) || (word1 && Word2) && ( !!(wordx) )  ...
        It may be as complex as you want

        returns a list of documents ID
        """
        pass

    def get_tree_from_query(query: str, open_parenthese : str = "(",close_parenthese : str = ")"):
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
            couple_liste.append((open_parenthese_indices.pop(i),cp))

        return couple_liste

class Node():
    def __init__(self, right_child = None, left_child = None, is_leaf = False, posting = None):
        self.right_child = right_child
        self.left_child = left_child
        self.is_leaf = is_leaf
        if self.is_leaf :
            if posting == None :
                raise ValueError(" if is leaf, posting must be a list")

    def set_right_child(self,right_child):
        self.right_child = right_child

    def set_left_child(self,left_child):
        self.left_child = left_child

    def get_result(self):
        pass

class ANDNode(Node):
    def __init__(self, right_child = None, left_child = None, is_leaf = False):
        Node.__init__(self, right_child = right_child, left_child = left_child, is_leaf = is_leaf)


    def get_result(self):
        if self.is_leaf :
            return self.posting
        return ANDNode.perform_AND_operation(self.right_child.get_result(),self.left_child.get_result(),BooleanModel.doc_id_index)

    @staticmethod
    def perform_AND_operation( posting1:list, posting2: list, doc_id_index: int  = 0 )  -> list :
        """
        posting = [(docID,frequency_word_doc,[position1, postions2, ...., postion_freq]), ...]
        doc_id_index (optional) int : the position of the "doc_id" in the tuple, by default 0 as above
        """
        n1 = len(posting1)
        n2 = len(posting2)
        docID1_pointer = 0
        docID2_pointer = 0
        posting_result = []
        while docID1_pointer < n1 :
            while docID2_pointer < n2 and posting2[docID2_pointer][doc_id_index] <= posting1[docID1_pointer][doc_id_index] :
                if posting1[docID1_pointer][doc_id_index] ==  posting2[docID2_pointer][doc_id_index] :
                    posting_result.append(posting1[docID1_pointer][doc_id_index])
                docID2_pointer += 1
            docID1_pointer += 1
        return posting_result

class ORNode(Node):
    def __init__(self, right_child = None, left_child = None, is_leaf = False):
        Node.__init__(self, right_child = right_child, left_child = left_child, is_leaf = is_leaf)

    def get_result(self):
        if self.is_leaf :
            return self.posting
        return ORNode.perform_OR_operation(self.right_child.get_result(),self.left_child.get_result(),BooleanModel.doc_id_index)

    @staticmethod
    def perform_OR_operation(posting1:list, posting2: list, doc_id_index: int  = 0 )  -> list :
        """
        posting = [(docID,frequency_word_doc,[position1, postions2, ...., postion_freq]), ...]
        doc_id_index (optional) int : the position of the "doc_id" in the tuple, by default 0 as above
        """
        n1 = len(posting1)
        n2 = len(posting2)
        docID1_pointer = 0
        docID2_pointer = 0
        posting_result = []
        while docID1_pointer < n1 :
            while docID2_pointer < n2 and posting2[docID2_pointer][doc_id_index] <= posting1[docID1_pointer][doc_id_index] :
                posting_result.append(posting2[docID2_pointer][doc_id_index])
                docID2_pointer += 1
            if posting1[docID1_pointer][doc_id_index] not in posting_result :
                posting_result.append(posting1[docID1_pointer][doc_id_index])
            docID1_pointer += 1
        while docID2_pointer < n2 :
            posting_result.append(posting2[docID2_pointer][doc_id_index])
            docID2_pointer += 1
        return posting_result


class NOTNode(Node):
    """must have only one child"""
    def __init__(self, right_child = None, left_child = None, is_leaf = False):
        Node.__init__(self, right_child = right_child, left_child = left_child, is_leaf = is_leaf)

    def get_result():
        if self.is_leaf :
            return self.posting
        else :
            pass


class BinaryTreeDecision():
    def __init__(self):
        self.root = None

    def verify_request():
        pass

    def get_result():
        return self.root.get_result()


if __name__ == "__main__" :
    posting1 = [(1,),(3,),(7,),(8,),(10,),(15,)]
    posting2 = [(1,),(4,),(7,),(9,),(10,),(11,),(15,),(16,),(18,),(20,)]
    # print(BooleanModel.perform_OR_operation(posting1,posting2))
    query = "((((((s))))))"
    print(BooleanModel.get_tree_from_query(query))
