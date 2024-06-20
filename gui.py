import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from start import UVSim, load_program_from_file

class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.uvsim = UVSim()
        self.uvsim.set_gui(self)
        self.create_widgets()
        self.program = []

    def create_widgets(self):
        self.root.title("UVSim")

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.load_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.open_button = tk.Button(self.toolbar, text="Open File", command=self.load_file)
        self.open_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.run_button = tk.Button(self.toolbar, text="Run", command=self.run_program)
        self.run_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.stop_button = tk.Button(self.toolbar, text="Stop", command=self.stop_program)
        self.stop_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.main_panel = tk.Frame(self.root)
        self.main_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.program_frame = tk.Frame(self.main_panel)
        self.program_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.program_label = tk.Label(self.program_frame, text="Program Instructions")
        self.program_label.pack(side=tk.TOP, anchor=tk.W)

        self.program_text = tk.Text(self.program_frame, wrap=tk.NONE)
        self.program_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.memory_frame = tk.Frame(self.main_panel)
        self.memory_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.memory_label = tk.Label(self.memory_frame, text="Memory Display")
        self.memory_label.pack(side=tk.TOP, anchor=tk.W)

        self.memory_tree = ttk.Treeview(self.memory_frame, columns=("Address", "Value"), show="headings", height=10)
        self.memory_tree.heading("Address", text="Address")
        self.memory_tree.heading("Value", text="Value")
        self.memory_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        self.status_frame = tk.Frame(self.memory_frame)
        self.status_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.accumulator_label = tk.Label(self.status_frame, text="Accumulator: [0000]")
        self.accumulator_label.pack(side=tk.TOP, anchor=tk.W)

        self.pc_label = tk.Label(self.status_frame, text="Program Counter: [0000]")
        self.pc_label.pack(side=tk.TOP, anchor=tk.W)

        self.status_label = tk.Label(self.status_frame, text="Status: Ready")
        self.status_label.pack(side=tk.TOP, anchor=tk.W)

        self.status_bar = tk.Label(self.root, text="Status: Ready", bd=2, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.config(font=("Helvetica", 12))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_file(self):
        filename = filedialog.askopenfilename(title="Open File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if filename:
            self.program = load_program_from_file(filename)
            if not self.program:
                messagebox.showerror("Error", "No valid instructions found in the file.")
                return
            self.uvsim.load_program(self.program)
            self.display_program(self.program)
            self.display_memory()
            self.status_label.config(text="Status: Program Loaded")
            self.status_bar.config(text="Status: Program Loaded")

    def display_program(self, program):
        self.program_text.delete(1.0, tk.END)
        for instruction in program:
            self.program_text.insert(tk.END, f"{instruction:04}\n")

    def display_memory(self):
        for i in self.memory_tree.get_children():
            self.memory_tree.delete(i)
        for address, value in enumerate(self.uvsim.memory):
            self.memory_tree.insert("", tk.END, values=(address, value))

    def run_program(self):
        if not self.uvsim.running:
            self.uvsim.load_program(self.program)
        self.uvsim.run()
        self.status_label.config(text="Status: Running")
        self.status_bar.config(text="Status: Running")

    def stop_program(self):
        self.uvsim.running = False
        self.status_label.config(text="Status: Stopped")
        self.status_bar.config(text="Status: Stopped")

    def show_about(self):
        messagebox.showinfo("About", "UVSim - UVU Simulator")

    def display_message(self, message):
        messagebox.showinfo("Information", message)

    def update_status(self):
        self.accumulator_label.config(text=f"Accumulator: [{self.uvsim.accumulator:04}]")
        self.pc_label.config(text=f"Program Counter: [{self.uvsim.pc:04}]")
        self.display_memory()

def main():
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
