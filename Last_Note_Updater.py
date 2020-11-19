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
    query = define_query
    note_id = invoke('findNotes', query=query)
    notes_info = invoke('notesInfo', notes=note_id)
    last_added_note.delete(0.0, END)
    last_added_note.insert(END, notes_info[-1]['fields'][field_to_read]['value'])
    search()


def search():
    # output.delete(0.0, END)
    dic_query = last_added_note.get("1.0", END)
    print(dic_query)
    result_query = query_dict(loaded_dict, dic_query.rstrip("\n"))
    print(result_query)
    # output.insert(END, result_query)
    plot_results(result_query)


def dummy():
    # dummy function does nothing
    print("Activated dummy function!")


def plot_results(results_list):
    clear_frame()
    step_res = 0
    set_row = 10
    print(f"Results: {len(results_list)}")
    for c, result in enumerate(results_list):
        print(f"Lines inside {c}: {len(result)}")
        Label(frame_results, text=f"Definition {c}: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=c+set_row+step_res, column=0)
        set_def = c+set_row+step_res+1
        for i, element in enumerate(result):
            print(element)
            # new_ele = re.sub('。「.*$', "", element)  # should remove the example sentences
            new_ele = element
            Button(frame_results, text=f"{new_ele}", fg="black", width=320, command=lambda s=new_ele: update_note(s), wraplength=310).grid(row=set_def+i, column=0, columnspan=4)
        set_row = (c+set_row+step_res)-c
        step_res = len(result)


def clear_frame():
    for frame_child in frame_results.winfo_children():
        frame_child.destroy()


def screen_w_size():
    print(root.winfo_screenwidth())
    print(root.winfo_width())


def update_note(line):
    query = define_query
    note_id = invoke('findNotes', query=query)
    notes_info = invoke('notesInfo', notes=note_id)
    def_jp_update = line
    if notes_info[-1]['fields'][field_to_add]['value'] == '':
        noteUpdate = {'id': notes_info[-1]['noteId'], 'fields': {field_to_add: f"{def_jp_update}"}}
    else:
        noteUpdate = {'id': notes_info[-1]['noteId'], 'fields': {field_to_add: f"{notes_info[-1]['fields'][field_to_add]['value']}<br>{def_jp_update}"}}
    invoke('updateNoteFields', note=noteUpdate)


# Load Dictionaries
list_of_term_banks = get_file_list(dict_path)
loaded_dict = load_dict(list_of_term_banks)

# Set relevant fields
field_to_read = "Focus"
field_to_add = "Def Jp"
define_query = "added:1"

# Color
bg_color = "#edd1b0"  # Peach

# window
root = Tk()
root.title("It works, kinda..")
root.configure(background=bg_color)
HEIGHT = root.winfo_screenheight()
WIDTH = root.winfo_screenwidth()
# Responsive grid
root.columnconfigure(0, minsize=80, weight=1)
root.columnconfigure(1, minsize=80, weight=1)
root.columnconfigure(2, minsize=80, weight=1)
root.columnconfigure(3, minsize=80, weight=1)
root.resizable(False, True)
root.geometry(f"320x{HEIGHT}+{WIDTH-325}+0")
# root.rowconfigure(0, weight=1)

#frames
frame_results = Frame(root, bg=bg_color)
frame_results.grid(row=10, column=0, columnspan=4)
frame_results.columnconfigure(0, minsize=80, weight=1)
frame_results.columnconfigure(1, minsize=80, weight=1)
frame_results.columnconfigure(2, minsize=80, weight=1)
frame_results.columnconfigure(3, minsize=80, weight=1)

# Clip board thing
Label(root, text="Clipboard: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=1, column=0)
clipboard_text = Text(root, width=240, height=1, wrap=WORD,  bg="white")
clipboard_text.grid(row=1, column=1, columnspan=3)

# Get Most recent note textbox
Label(root, text="Note: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=2, column=0)
last_added_note = Text(root, width=240, height=1, wrap=WORD,  bg="white")
last_added_note.grid(row=2, column=1, columnspan=4)

# Menu Buttons
Button(root, text="Last Note", width=80, command=get_notes).grid(row=0, column=0)
Button(root, text="Clipboard", width=80, command=get_clipboard).grid(row=0, column=1)
Button(root, text="Search", width=80, command=dummy).grid(row=0, column=2)
Button(root, text="Exit", width=80, command=exit_app).grid(row=0, column=3)

# run the app
root.mainloop()
