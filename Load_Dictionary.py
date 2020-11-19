import os
import json
import re

file_path = os.getcwd()
print(file_path)
dict_path = file_path + "\Dictionaries\大辞林"
print(dict_path)
def get_file_list(path):
    arr = os.listdir(path)
    # print(arr)
    arr2 = [None]*len(arr)
    for i, each in enumerate(arr2):
        arr2[i]='term_bank_{}.json'.format(i)
    arr2[0] = 'index.json'
    # print(arr2)
    return arr2


def read_json(list, query):
    # for file in list:
    #     f = open()
    # with open("D:\Python\Scripts\Python\AnkiConnectUtils\Dictionary\大辞林\\term_bank_1.json") as f:
    #     data = json.load(f)

    with open("{}\\{}".format(dict_path,list[2]), encoding="utf-8") as file:
        data = json.load(file)
    print(list[2],len(data), type(data))
    # print(json.dumps(data, indent=4))

    result = []
    for i,entry in enumerate(data):
        if query == entry[0]:
            # print(i)
            print(entry[0], entry[1])
            def_str = ' '.join(map(str, entry[5]))
            def_list = def_str.split('\n')
            def_list += def_list.pop()

            for i,item in enumerate(def_list, start=1):
                print("#{}. {}".format(i,item))

def load_dict(list_of_files):
    all_jsons =[]
    for i,file in enumerate(list_of_files):
        with open("{}\\{}".format(dict_path,list_of_files[i]), encoding="utf-8") as file:
            data = json.load(file)
            all_jsons.append(data)
    print("-----\nLoaded ",len(all_jsons), 'json files\n-----')
    for i,list in enumerate(all_jsons):
        print(list_of_files[i],'. ',len(all_jsons[i]), 'entries.')
    # print(all_jsons)
    return all_jsons


def query_dict(list_entries, query):
    result = []
    for bank in list_entries:
        for entry in bank:
            if entry[0] == query:
                # print(i)
                print("Result(s) for {} {}".format(entry[0], entry[1]))
                # result.insert(0,[entry[0]])
                # print(result[0])
                def_str = ' '.join(map(str, entry[5]))
                def_list = def_str.split('\n')
                def_list += def_list.pop()
                def_list.insert(0,f"{entry[0]} {entry[1]}")
                # for i, item in enumerate(def_list, start=1):
                #     print("#{}. {}".format(i, item))
                result.append(def_list)
    print(result)
    return result


def result_choose(result):
    print(len(result))
    for i,entry in enumerate(result):
        print(f"Result #{i}:")
        for c,d in enumerate(entry):
            print(f"\t#{c}. {d}")

# def search(query):
# query = '麁飯'
# query = '有る'



list = get_file_list(dict_path)
# print(list)
# read_json(list,query)
d_ent = load_dict(list)
print("-------")
# print("Type word to search:")
# query = input()


query = '好き'
res = query_dict(d_ent,query)
result_choose(res)