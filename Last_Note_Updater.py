from tkinter import *
import pyperclip
from Anki_Connect_Function import invoke
from Load_Dictionaries_2 import *


# Exit command
def exit_app():
    root.destroy()
    exit()


# Get clipboard
def get_clipboard():
    clipboard_text.delete(0.0, END)
    clipboard_text.insert(END, pyperclip.paste())


def get_notes():
    query = 'added:1'
    note_id = invoke('findNotes', query=query)
    notes_info = invoke('notesInfo', notes=note_id)
    last_added_note.delete(0.0, END)
    last_added_note.insert(END, notes_info[-1]['fields']['Focus']['value'])
    search()


def search():
    # output.delete(0.0, END)
    dic_query = last_added_note.get("1.0", END)
    print(dic_query)
    result_query = query_dict(loaded_dict, dic_query.rstrip("\n"))
    print(result_query)
    # output.insert(END, result_query)
    updater_print_results(result_query)


def dummy():
    # dummy funtion does nothing
    print("Activated dummy funtion!")


def updater_print_results(results_list):
    step_res = 0
    print(f"Results: {len(results_list)}")
    for c, result in enumerate(results_list):
        print(f"Lines inside {c}: {len(result)}")
        Label(root, text=f"Definition {c+1}: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=c+11+step_res, column=0)

        for i, element in enumerate(result, start=c+12+step_res):
            print(element)
            new_ele = re.sub('。「.*$', "", element)  # should remove the example sentences
            Button(root, text=f"{new_ele}", width=320, command=lambda s=new_ele: update_note(s), wraplength=310).grid(row=c+i, column=0, columnspan=4)
            # Label(root, text=f"Line {i}: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=i, column=2)
            step_res = len(result)


def screen_w_size():
    print(root.winfo_screenwidth())
    print(root.winfo_width())


def update_note(line):
    query = 'added:1'
    note_id = invoke('findNotes', query=query)
    notes_info = invoke('notesInfo', notes=note_id)
    def_jp_update = line
    if notes_info[-1]['fields']['Def Jp']['value']=='':
        noteUpdate = {'id': notes_info[-1]['noteId'], 'fields': {'Def Jp': f"{def_jp_update}"}}
    else:
        noteUpdate = {'id': notes_info[-1]['noteId'], 'fields': {'Def Jp': f"{notes_info[-1]['fields']['Def Jp']['value']}<br>{def_jp_update}"}}
    invoke('updateNoteFields', note=noteUpdate)


# Load Dictionaries
list_of_term_banks = get_file_list(dict_path)
loaded_dict = load_dict(list_of_term_banks)


# Color
bg_color = "#edd1b0"  # Peach

# window
root = Tk()
root.title("Mine Helper Crappy stages")
root.configure(background=bg_color)
HEIGHT = root.winfo_screenheight()
WIDTH = root.winfo_screenwidth()
root.geometry(f"320x{HEIGHT}")

# Responsive grid
root.columnconfigure(0, minsize=80, weight=1)
root.columnconfigure(1, minsize=80, weight=1)
root.columnconfigure(2, minsize=80, weight=1)
root.columnconfigure(3, minsize=80, weight=1)
root.resizable(False, True)
root.geometry(f"320x{HEIGHT}+{WIDTH-325}+0")
# root.rowconfigure(0, weight=1)


# Clip board thing
Label(root, text="Clipboard: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=1, column=0)
clipboard_text = Text(root, width=240, height=1, wrap=WORD,  bg="white")
clipboard_text.grid(row=1, column=1, columnspan=3)

# Get Most recent note textbox
Label(root, text="Note: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=2, column=0)
last_added_note = Text(root, width=240, height=1, wrap=WORD,  bg="white")
last_added_note.grid(row=2, column=1, columnspan=4)


# Buttons
Button(root, text="Last Note", width=80, command=get_notes).grid(row=0, column=0)
Button(root, text="Clipboard", width=80, command=get_clipboard).grid(row=0, column=1)
Button(root, text="Search", width=80, command=dummy).grid(row=0, column=2)
Button(root, text="Exit", width=80, command=exit_app).grid(row=0, column=3)


# run the app
root.mainloop()
