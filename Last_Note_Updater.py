from tkinter import *
from tkinter import ttk
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
    dic_query = last_added_note.get("1.0", END)
    print(f"\nNote: {dic_query}")
    result_query = query_dict(loaded_dict, dic_query.rstrip("\n"))
    plot_results(result_query)


def dummy():
    # dummy function does nothing
    print("Activated dummy function!")


def plot_results(results_list):
    clear_frame()
    step_res = 0
    set_row = 10
    print(f"Number of Results: {len(results_list)}")
    for c, result in enumerate(results_list):
        print(f"Result {c+1}: ")
        Label(canvas_frame, text=f"Definition {c+1}: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=c+set_row+step_res, column=0)
        set_def = c+set_row+step_res+1
        for i, element in enumerate(result):
            print(f"\t{element}")
            # new_ele = re.sub('。「.*$', "", element)  # should remove the example sentences
            new_ele = element
            Button(canvas_frame, text=f"{new_ele}", fg="black", width=42, command=lambda s=new_ele: update_note(s), wraplength=280).grid(row=set_def+i, column=0, columnspan=4, sticky=W)
        set_row = (c+set_row+step_res)-c
        step_res = len(result)
    canvas_frame.bind("<Configure>", onFrameConfigure)


def onFrameConfigure(event):
    results_canvas.configure(scrollregion=results_canvas.bbox("all"))


def clear_frame():
    for frame_child in canvas_frame.winfo_children():
        frame_child.destroy()


def screen_w_size():
    print(root.winfo_screenwidth())
    print(f"width{root.winfo_width()}")
    print(f"height{root.winfo_height()}")


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
root.geometry(f"320x650+{WIDTH-330}+0")

#frames
frame_results = Frame(root, bg=bg_color, width=320)
frame_results.grid(row=10, column=0, columnspan=4, sticky=W)
frame_results.columnconfigure(0, minsize=80, weight=1)
frame_results.columnconfigure(1, minsize=80, weight=1)
frame_results.columnconfigure(2, minsize=80, weight=1)
frame_results.columnconfigure(3, minsize=80, weight=1)

#canvas
results_canvas = Canvas(frame_results, height=550, bg=bg_color)
results_canvas.grid(row=0, column=0, columnspan=4)
results_canvas.columnconfigure(0, minsize=80, weight=1)
results_canvas.columnconfigure(1, minsize=80, weight=1)
results_canvas.columnconfigure(2, minsize=80, weight=1)
results_canvas.columnconfigure(3, minsize=80, weight=1)


# scrollbar
scrollbar = ttk.Scrollbar(frame_results, orient=VERTICAL, command=results_canvas.yview)
scrollbar.grid(column=3, row=0, sticky=(N,E,S))

#configure canvas
results_canvas.configure(yscrollcommand=scrollbar.set)

#frame inside canvas
canvas_frame = Frame(results_canvas, bg=bg_color)
canvas_frame.columnconfigure(0, minsize=80, weight=1)
canvas_frame.columnconfigure(1, minsize=80, weight=1)
canvas_frame.columnconfigure(2, minsize=80, weight=1)
canvas_frame.columnconfigure(3, minsize=80, weight=1)

# adding inside frame in a window in canvas
results_canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

# Clip board thing
Label(root, text="Clipboard: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=1, column=0)
clipboard_text = Text(root, width=240, height=1, wrap=WORD,  bg="white")
clipboard_text.grid(row=1, column=1, columnspan=3)

# Get Most recent note textbox
Label(root, text="Note: ", bg=bg_color, fg="black", font="none 10 bold").grid(row=2, column=0)
last_added_note = Text(root, width=240, height=1, wrap=WORD,  bg="white")
last_added_note.grid(row=2, column=1, columnspan=3)

# Menu Buttons
Button(root, text="Last Note", width=80, command=get_notes).grid(row=0, column=0)
Button(root, text="Clipboard", width=80, command=get_clipboard).grid(row=0, column=1)
Button(root, text="Search", width=80, command=screen_w_size).grid(row=0, column=2)
Button(root, text="Exit", width=80, command=exit_app).grid(row=0, column=3)

# run the app
root.mainloop()
