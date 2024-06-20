from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
window = tk.Tk()
window.title("GUI Practice")
window.geometry("500x500")



'''
class Redirect():
    def __init__(self, widget):
        self.widget = widget

    def write(self, text_window):
        self.widget.insert('end', text_window)
'''
def file_open(*args):
    text_window = Text(window, bg="white",width=50, height=20)
    text_window.place(x=50, y=70)   
    open_button = Button(window, text="Open File", command=file_open)
    open_button.grid(row=0, column=0, padx=1)
    text_window.delete('1.0', END)
    filePath = askopenfilename(
        initialdir='C:/', title='Select a File', filetype=(("Text File", ".txt"), ("All Files", "*.*")))
    
    program = []
    with open(filePath, 'r') as file:
        for line in file:
            line = line.strip()
            program.append(int(line))     
        fileContents = file.read()
    text_window.insert(INSERT, fileContents)
    print(filePath)
    
    return program    

