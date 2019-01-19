from global_variables import path_cacm_all
import re

def get_cacm_data_as_dict(file_name: str) -> dict:
    with open(file_name,"r") as f :
        i = 0
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
    return documents

def preprocess_title(title:str):
    # A LOT OF WORK TO DO HERE
    return(re.sub("\n"," ",title))



if __name__ == "__main__" :
    doc = get_data(path_cacm_all)
    print(len(doc))
