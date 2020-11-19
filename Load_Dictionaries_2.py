import os
import json
import re

# Getting dictionary paths
file_path = os.getcwd()
dict_path = file_path + "\Dictionaries\大辞林"

# Creates a list of the dictionary files, fixing the order
def get_file_list(path):
    arr = os.listdir(path)
    # print(arr)
    arr2 = [None]*len(arr)
    for i in range(len(arr2)):
        arr2[i]=f'term_bank_{i}.json'
    arr2[0] = 'index.json'
    # print(arr2)
    return arr2


# Load Dictionaries based on the list of files into memory
def load_dict(list_of_files):
    all_jsons =[]
    for i,file in enumerate(list_of_files):
        with open("{}\\{}".format(dict_path,list_of_files[i]), encoding="utf-8") as file:
            data = json.load(file)
            all_jsons.append(data)
    print("-----\nLoaded ",len(all_jsons), 'json files\n-----')
    for i, list_item in enumerate(all_jsons):
        print(list_of_files[i],'. ',len(list_item), 'entries.')
    # print(all_jsons)
    return all_jsons


# Query Dictionary
def query_dict(list_entries, query):
    result = []
    for bank in list_entries:
        for entry in bank:
            if entry[0] == query:
                # print(i)
                # print("Result(s) for {} ({})".format(entry[0], entry[1]))
                # result.insert(0,[entry[0]])
                # print(result[0])
                def_str = ' '.join(map(str, entry[5]))
                def_list = def_str.split('\n')
                def_list += def_list.pop()

                ## if you wan to add the term and reading in the results
                # def_list.insert(0,f"{entry[0]} ")
                # def_list.insert(1, f"{entry[1]}")
                result.append(def_list)
    print(len(result))
    return result

# Print results decently
def print_results(results_list):
    for result in results_list:
        for element in result:
            print(element)
            new_ele = re.sub('\。\「.*$', "", element)
            print(new_ele)
