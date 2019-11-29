
from math import inf
import tkinter
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror

def prefix_func(i, pattern):
    if i == 0:
        return 0
    else:
        max = -inf
        sub = pattern[:(i+1)]
        for j in range(len(sub) - 1):
            if sub[:j+1] == sub[-j-1:] and len(sub[:j+1]) > max:
                max = len(sub[:j+1])
        if max == -inf:
            return 0
        else:
            return max


def get_pi(pattern):
    pi = []
    for i in range(len(pattern)):
        pi.append(prefix_func(i, pattern))
    return pi

def kmp(text, pattern):
    s= []
    pi = get_pi(pattern)
    j = 0
    i = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                s.append(i - j)
                j = 0
        else:
            if j != 0:
                j = pi[j - 1]
            else:
                i += 1
    return s


def kmp_search():
    t = text.get('1.0', tkinter.END)
    p = pattern.get()
    if with_reg.get() == 0:
        t = t.lower()
        p = p.lower()
    s = kmp(t, p)
    text.tag_remove("bold", 1.0, tkinter.END)
    for i in s:
        text.tag_add("bold", "1.0+" + str(i) + "c", "1.0+" + str(i + len(p)) + "c")
        text.tag_config('bold', foreground="red")
    show_message("Search", "Found: " + str(len(s)))


def show_message(title, message):
    tkinter.messagebox.showinfo(title, message)

FILE_NAME = tkinter.NONE

def new_file():
    global FILE_NAME
    FILE_NAME = "Untitled"
    text.delete('1.0', tkinter.END)

def save_file():
    data = text.get('1.0', tkinter.END)
    out = open(FILE_NAME, 'w')
    out.write(data)
    out.close()

def save_as():
    out = asksaveasfile(mode='w', defaultextension='.txt')
    data = text.get('1.0', tkinter.END)
    try:
        out.write(data.rstrip())
    except Exception:
        showerror(title="Oops!", message="Unable to save file....")

def open_file():
    global FILE_NAME
    inp = askopenfile(mode="r")
    if inp is None:
        return
    FILE_NAME = inp.name

    data = inp.read()
    text.delete('1.0', tkinter.END)
    text.insert('1.0', data)

root = tkinter.Tk()
root.title("KMP and text editor")
root.minsize(width=645, height=430)
root.maxsize(width=645, height=430)

pattern_lb = tkinter.Label(root, text="Search: ")
pattern_lb.grid(row=0, column=0, pady=5)

pattern = tkinter.StringVar()

pattern_entry = tkinter.Entry(root, textvariable=pattern)
pattern_entry.grid(row=0, column=1, pady=5)

with_reg = tkinter.IntVar()

with_reg_chkb = tkinter.Checkbutton(text="with register", variable=with_reg)
with_reg_chkb.grid(row=0, column=2, pady=5)

search_btn = tkinter.Button(root, text="Search", command=kmp_search)
search_btn.grid(row=0, column=3, pady=5)

text = tkinter.Text(root)
text.grid(row=1, column=0, columnspan=30)

menuBar = tkinter.Menu(root)
fileMenu = tkinter.Menu()
fileMenu.add_command(label="New", command=new_file)
fileMenu.add_command(label="Open", command=open_file)
fileMenu.add_command(label="Save", command=save_file)
fileMenu.add_command(label="Save As", command=save_as)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
menuBar.add_cascade(label="File", menu=fileMenu)

root.config(menu=menuBar)
root.mainloop()
