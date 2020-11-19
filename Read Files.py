import os

file_path = os.getcwd()
vid_ext = "mkv"
sub_ext = "srt"


def get_file_list(path, v_format, s_format):
    print(f'Getting lists for "{vid_ext}" and "{sub_ext}" files in "{file_path}"...')
    vid_arr = []
    subs_arr = []
    arr = os.listdir(path)
    for i, name in enumerate(arr):
        if name.endswith('.' + v_format):
            vid_arr.append(name)
        elif name.endswith('.' + s_format):
            subs_arr.append(name)
    return vid_arr, subs_arr


def print_lists(lists):
    print("Printing lists...")
    for l1, list in enumerate(lists, start=1):
        print(f"List {l1}")
        for l2, item in enumerate(list,start=1):
            print(f"\t{l2}.{item}")


lists = get_file_list(file_path, vid_ext, sub_ext)
print_lists(lists)

arr = os.listdir(file_path + "\\Dictionaries")

print(arr)
print('Press Enter key to exit')
input()