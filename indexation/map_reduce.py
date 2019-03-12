from saver import add_1_termid_postings_to_file,\
                    get_1_termid_postings_from_fileline,\
                    save_new_termid_posting

import os
from collections import OrderedDict

def merge_postings(postings1, postings2):
    return sorted(set(postings1).union(set(postings2)))

def get_file_size(f):
    return f.seek(0,2)

def aggregate_2_termid_postings(file1_path, file2_path, result_path, max_memory_size, aggregating_level):
    file1 = open(file1_path,"r")
    file2 = open(file2_path,"r")
    end_file1 = False
    end_file2 = False
    termid1, postings1 = get_1_termid_postings_from_fileline(next(file1),sep = " ")
    termid2, postings2 = get_1_termid_postings_from_fileline(next(file2),sep = " ")
    result_file_name = result_path+"/"+str(aggregating_level)+"_"+str(min(termid1,termid2))+".txt"
    result_file = open(result_file_name,"w")
    liste_of_result_files = [result_file_name]
    while not(end_file1) and not(end_file2):
        is_new_file = False
        if get_file_size(result_file) > max_memory_size :
            result_file.close()
            is_new_file = True
        if termid1 == termid2 :
            termid = termid1
            new_posting = merge_postings(postings1, postings2)
            # print(termid, new_posting)
            try :
                termid1, postings1 = get_1_termid_postings_from_fileline(next(file1),sep = " ")
            except StopIteration :
                end_file1 = True
            try :
                termid2, postings2 = get_1_termid_postings_from_fileline(next(file2),sep = " ")
            except StopIteration :
                end_file2 = True
        elif termid1 < termid2 :
            termid, new_posting = termid1, postings1
            try :
                termid1, postings1 = get_1_termid_postings_from_fileline(next(file1),sep = " ")
            except StopIteration :
                end_file1 = True
        else :
            termid, new_posting = termid2, posting2
            try :
                termid2, postings2 = get_1_termid_postings_from_fileline(next(file2),sep = " ")
            except StopIteration :
                end_file2 = True
        if is_new_file :
            result_file_name = result_path+"/"+str(aggregating_level)+"_"+str(termid)+".txt"
            result_file = open(result_file_name,"w")
            liste_of_result_files.append(result_file_name)
        add_1_termid_postings_to_file(result_file, termid, new_posting, sep = " ")

    while not(end_file1):
        add_1_termid_postings_to_file(result_file, termid1, postings1, sep = " ")
        is_new_file = False
        if get_file_size(result_file) > max_memory_size :
            result_file.close()
            is_new_file = True
        try :
            termid1, postings1 = get_1_termid_postings_from_fileline(next(file1),sep = " ")
        except StopIteration :
            end_file1 = True
        if is_new_file :
            result_file_name = result_path+"/"+str(aggregating_level)+"_"+str(termid1)+".txt"
            result_file = open(result_file_name,"w")
            liste_of_result_files.append(result_file_name)


    while not(end_file2):
        is_new_file = False
        if get_file_size(result_file) > max_memory_size :
            result_file.close()
            is_new_file = True
        try :
            termid2, postings2 = get_1_termid_postings_from_fileline(next(file2),sep = " ")
        except StopIteration :
            end_file2 = True
        if is_new_file :
            result_file_name = result_path+"/"+str(aggregating_level)+"_"+str(termid2)+".txt"
            result_file = open(result_file_name,"w")
            liste_of_result_files.append(result_file_name)
        # if termid2 == "1" :
            # print(1,"  ",postings2)

        add_1_termid_postings_to_file(result_file, termid2, postings2, sep = " ")

    file1.close()
    file2.close()
    result_file.close()
    return liste_of_result_files
def get_file_path(file_name):
    return "/".join(file_name.split("/")[:-1])

def get_level_from_file_name(file_name):
    file_name = file_name.split("/")[-1]
    i = file_name.index("_")
    return int(file_name[:i]),file_name[i+1:]

def aggregate_list_of_termid_postings(list_of_file_paths, result_path, max_memory_size):
    sorted_list_of_file_paths = sorted(list_of_file_paths)
    sorted_list_of_file_paths_by_begginings_letters = sorted(list_of_file_paths, \
                                                        key = lambda file_name : get_level_from_file_name(file_name)[1])
    aggregating_level =  get_level_from_file_name(list_of_file_paths[-1])[0] + 1
    liste_of_useful_files = []
    liste_of_temp_files = set(list_of_file_paths)
    i = 0
    while i < (len(sorted_list_of_file_paths_by_begginings_letters)-1):
        f1 = sorted_list_of_file_paths_by_begginings_letters[i]
        f2 = sorted_list_of_file_paths_by_begginings_letters[i+1]
        liste_of_temp_files.add(f1)
        liste_of_temp_files.add(f2)
        if  get_level_from_file_name(f1)[0] == get_level_from_file_name(f2)[0] :
            liste_of_useful_files.append(f1)
            i += 1
            continue
        else :
            new_files = aggregate_2_termid_postings(f1, f2, result_path, max_memory_size,aggregating_level)
            aggregating_level += 1
            sorted_list_of_file_paths_by_begginings_letters[i:i+2] = new_files
            sorted_list_of_file_paths_by_begginings_letters = sorted(sorted_list_of_file_paths_by_begginings_letters, \
                                                                key = lambda file_name : get_level_from_file_name(file_name)[1])

    liste_of_useful_files.append(sorted_list_of_file_paths_by_begginings_letters[-1])
    liste_of_temp_files = liste_of_temp_files.difference(liste_of_useful_files)
    for ff in liste_of_temp_files :
        os.remove(ff)
    for usefull_file in liste_of_useful_files :
        new_name = result_path+"/"+str(get_level_from_file_name(usefull_file)[1])
        print(new_name)
        os.rename(usefull_file,new_name)
    return liste_of_useful_files

if __name__ == "__main__" :
    liste1 = {"1":["0","1","2","4","5","6"], "2" :["0","1","4","5","6","7","8","9"],"3":["1","2","3","4","8","9","10","12","45"]}
    liste1 = OrderedDict(sorted(liste1.items()))
    liste2 = {"1":["0","1","4","5","6","7","8","9"], "3" :["0","1","4","5","6","7","8","9"],"4":["1","2","3","4","8","9","10","12","45"]}
    liste2 = OrderedDict(sorted(liste2.items()))
    liste3 = {"1":["0","1","2","4","5","6"], "2" :["0","1","4","5","6","7","8","9"],"3":["1","2","3","4","8","9","10","12","45"]}
    liste3 = OrderedDict(sorted(liste1.items()))
    liste4 = {"1":["0","1","4","5","6","7","8","9"], "3" :["0","1","4","5","6","7","8","9"],"4":["1","2","3","4","8","9","10","12","45"]}
    liste4 = OrderedDict(sorted(liste2.items()))
    result_path = "test/result"
    file1_path = "1_1.txt"
    file2_path = "2_1.txt"
    file3_path = "3_1.txt"
    file4_path = "4_1.txt"
    save_new_termid_posting(liste1, "col1", result_path, file1_path)
    save_new_termid_posting(liste2, "col1", result_path, file2_path)
    save_new_termid_posting(liste3, "col1", result_path, file3_path)
    save_new_termid_posting(liste4, "col1", result_path, file4_path)
    list_of_file_paths = [result_path+'/'+file1_path,result_path+'/'+file2_path, result_path+'/'+file3_path, result_path+'/'+file4_path]
    a = aggregate_list_of_termid_postings(list_of_file_paths, result_path, 0)
    print(a)
