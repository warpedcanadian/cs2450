import tkinter as tk
from tkinter import ttk
from utils import load_program_from_file
from tkinter import filedialog, messagebox


def load_file(program_frame):
    filename = filedialog.askopenfilename(title="Open File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if filename:
        program = load_program_from_file(filename)
        if not program:
            messagebox.showerror("Error", "No valid instructions found in the file.")
            return
        display_program(program, program_frame)
        display_memory()
        # status_label.config(text="Status: Program Loaded")
        # status_bar.config(text="Status: Program Loaded")
        return program


def display_program(program, program_frame):

    program_text = tk.Text(program_frame, wrap=tk.NONE)
    program_text.delete(1.0, tk.END)
    for instruction in program:
        program_text.insert(tk.END, f"{instruction:04}\n")


def display_memory():
    pass


def show_about():
    print('show about')


def run_program():
    pass
# def stop_program():
#     pass


def create_widget(root):
    root.title("UVSim")

    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=load_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    edit_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Edit", menu=edit_menu)

    help_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_about)

    toolbar = tk.Frame(root)
    toolbar.pack(side=tk.TOP, fill=tk.X)

    open_button = tk.Button(toolbar, text="Open File", command=load_file)
    open_button.pack(side=tk.LEFT, padx=2, pady=2)

    run_button = tk.Button(toolbar, text="Run", command=run_program)
    run_button.pack(side=tk.LEFT, padx=2, pady=2)

    # stop_button = tk.Button(toolbar, text="Stop", command=stop_program)
    # stop_button.pack(side=tk.LEFT, padx=2, pady=2)

    main_panel = tk.Frame(root)
    main_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    program_frame = tk.Frame(main_panel)
    program_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    program_label = tk.Label(program_frame, text="Program Instructions")
    program_label.pack(side=tk.TOP, anchor=tk.W)

    program_text = tk.Text(program_frame, wrap=tk.NONE)
    program_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    memory_frame = tk.Frame(main_panel)
    memory_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    memory_label = tk.Label(memory_frame, text="Memory Display")
    memory_label.pack(side=tk.TOP, anchor=tk.W)

    memory_tree = ttk.Treeview(memory_frame, columns=("Address", "Value"), show="headings", height=10)
    memory_tree.heading("Address", text="Address")
    memory_tree.heading("Value", text="Value")
    memory_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    status_frame = tk.Frame(memory_frame)
    status_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    accumulator_label = tk.Label(status_frame, text="Accumulator: [0000]")
    accumulator_label.pack(side=tk.TOP, anchor=tk.W)

    pc_label = tk.Label(status_frame, text="Program Counter: [0000]")
    pc_label.pack(side=tk.TOP, anchor=tk.W)

    status_label = tk.Label(status_frame, text="Status: Ready")
    status_label.pack(side=tk.TOP, anchor=tk.W)

    status_bar = tk.Label(root, text="Status: Ready", bd=2, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.config(font=("Helvetica", 12))
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)


def main():
    root = tk.Tk()
    create_widget(root)
    root.mainloop()


if __name__ == '__main__':
    main()
