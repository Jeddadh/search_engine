import os

def save_new_term_termid(term_termid,collection_name, file_path,file_name ="term_termid.txt",sep = " ",end_car = "\n"):
    f = open(file_path+"/"+file_name,"w")
    for term in term_termid :
        f.write(str(term)+sep+str(term_termid[term])+end_car)
    f.close()
def save_new_termid_posting(termid_postings, collection_name, file_path, file_name="termid_postings.txt",sep =" ", end_car ="\n"):
    f = open(file_path+"/"+file_name,"w")
    for termid in termid_postings :
        f.write(str(termid))
        for doc_id in termid_postings[termid]:
            f.write(sep)
            f.write(str(doc_id))
        f.write(end_car)
    f.close()

def save_new_docid_linktodoc(docid_linktodoc, collection_name, file_name):
    pass

def get_term_termid(file_name):
    term_termid = {}
    with open(file_name,"r") as f :
        for line in f :
            liste = line[:-1].split(' ')
            term = liste[0]
            termid = int(liste[1])
            term_termid[term] = termid
    return term_termid

def get_termid_posting(file_name):
    termid_postings = {}
    with open(file_name,"r") as f :
        for line in f :
            liste = line[:-1].split(' ')
            termid = int(liste[0])
            posting = liste[1:]
            termid_postings[termid] = [int(pos) for pos in posting]
    return termid_postings


def get_docid_linktodoc(collection_name, hash_value):
    pass

def add_1_termid_postings_to_file(file, termid, postings, sep, end_car = "\n"):
    """
    file : file object open in add mode
    sep : separateur
    """
    file.write(termid)
    for pos in postings :
        file.write(sep)
        file.write(str(pos))
    file.write(end_car)

def get_1_termid_postings_from_fileline(fileline, sep, end_car = "\n"):
    """
    """
    # print(fileline[:])
    split_line = fileline[:-1].split(sep)
    termid = split_line[0]
    postings = [int(x) for x in split_line[1:]]
    return termid, postings
