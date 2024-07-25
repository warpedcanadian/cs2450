import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from tkinter import ttk
from start import UVSim, load_program_from_file
import json
from tkinter.filedialog import asksaveasfile


def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = {
            "primary_color": "#4C721D",
            "off_color": "#FFFFFF"
        }
        save_config(config)
    return config


def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)


class UVSimGUI:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.primary_color = self.config['primary_color']
        self.off_color = self.config['off_color']
        self.uvsim = UVSim()
        self.uvsim.set_gui(self)
        self.create_widgets()
        self.apply_color_scheme()
        self.programs = {}
        # self.root.geometry("1280x600") 

    def create_widgets(self):
        self.root.title("UVSim")

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.load_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Convert to 6-Digit", command=self.convert_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Add Instruction", command=self.add_instruction)
        self.edit_menu.add_command(label="Delete Instruction", command=self.delete_instruction)
        self.edit_menu.add_command(label="Change Color Scheme", command=self.change_color_scheme)

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.run_button = tk.Button(self.toolbar, text="Run", command=self.run_program)
        self.run_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.stop_button = tk.Button(self.toolbar, text="Stop", command=self.stop_program)
        self.stop_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_button = tk.Button(self.toolbar, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.main_panel = tk.Frame(self.root)
        self.main_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(self.main_panel)
        self.notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

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

        self.accumulator_label = tk.Label(self.status_frame, text="Accumulator: [000000]")
        self.accumulator_label.pack(side=tk.TOP, anchor=tk.W)

        self.pc_label = tk.Label(self.status_frame, text="Program Counter: [000000]")
        self.pc_label.pack(side=tk.TOP, anchor=tk.W)

        self.status_label = tk.Label(self.status_frame, text="Status: Ready")
        self.status_label.pack(side=tk.TOP, anchor=tk.W)

        self.status_bar = tk.Label(self.root, text="Status: Ready", bd=2, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.config(font=("Helvetica", 12))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=1, pady=(0, 10))

        self.output_text = tk.Text(self.output_frame, wrap=tk.NONE, height=5)
        self.output_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

    def apply_color_scheme(self):
        style = ttk.Style()
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        fieldbackground="white")

        self.root.configure(bg=self.primary_color)
        self.toolbar.configure(bg=self.primary_color)
        self.run_button.configure(bg=self.primary_color, fg=self.off_color)
        self.stop_button.configure(bg=self.primary_color, fg=self.off_color)
        self.save_button.configure(bg=self.primary_color, fg=self.off_color)
        self.status_bar.configure(bg=self.primary_color, fg=self.off_color)

        self.memory_frame.configure(bg=self.primary_color)
        self.memory_label.configure(bg=self.primary_color, fg=self.off_color)
        self.memory_tree.configure(style="Treeview")

        self.status_frame.configure(bg=self.primary_color)
        self.accumulator_label.configure(bg=self.primary_color, fg=self.off_color)
        self.pc_label.configure(bg=self.primary_color, fg=self.off_color)
        self.status_label.configure(bg=self.primary_color, fg=self.off_color)

        self.output_frame.configure(bg=self.primary_color)
        self.output_text.configure(bg='white', fg='black')

    def change_color_scheme(self):
        primary_color = colorchooser.askcolor(title="Choose Primary Color")[1]
        off_color = colorchooser.askcolor(title="Choose Off-Color")[1]
        if primary_color and off_color:
            self.primary_color = primary_color
            self.off_color = off_color
            self.config['primary_color'] = self.primary_color
            self.config['off_color'] = self.off_color
            save_config(self.config)
            self.apply_color_scheme()

    def load_file(self):
        filenames = filedialog.askopenfilenames(title="Open File",
                                                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        for filename in filenames:
            with open(filename, 'r') as file:
                content = file.read()
            self.add_tab(filename, content)
            self.program = load_program_from_file(filename)
            if not self.program:
                messagebox.showerror("Error", "No valid instructions found in the file.")
                return
            self.uvsim.load_program(self.program)
            self.display_program(self.program)
            self.display_memory()
            self.status_label.config(text="Status: Program Loaded")
            self.status_bar.config(text="Status: Program Loaded")
        self.root.geometry("")  # Adjust window size to fit the new content

    def save_file(self):
        current_tab = self.notebook.select()
        file_path = self.notebook.tab(current_tab, "text")
        content = self.programs[file_path].get(1.0, tk.END).strip()
        with open(file_path, 'w') as file:
            file.write(content)

    def add_tab(self, filename, content):
        tab = tk.Frame(self.notebook)
        self.notebook.add(tab, text=filename)

        program_text = tk.Text(tab, wrap=tk.NONE, height=20)
        program_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        program_text.insert(tk.END, content)

        self.programs[filename] = program_text

    def convert_file(self):
        filename = filedialog.askopenfilename(title="Open 4-Digit File",
                                              filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if filename:
            with open(filename, 'r') as file:
                lines = file.readlines()

            new_lines = []
            for line in lines:
                line = line.strip()
                if UVSim.is_valid_instruction(line):
                    if len(line) == 5:  # Already has sign and 4 digits
                        new_line = f"{line[0]}0{line[1:]}"
                    elif len(line) == 4:  # No sign, 4 digits
                        new_line = f"+0{line}"
                    else:
                        messagebox.showerror("Error", "File contains invalid instructions.")
                        return
                    new_lines.append(new_line)
                else:
                    messagebox.showerror("Error", f"Invalid instruction '{line}' found.")
                    return

            new_filename = filedialog.asksaveasfilename(title="Save 6-Digit File",
                                                        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            if new_filename:
                with open(new_filename, 'w') as new_file:
                    for line in new_lines:
                        new_file.write(f"{line}\n")
                messagebox.showinfo("Success", f"File converted and saved as {new_filename}")

    def add_instruction(self):
        new_instruction = simpledialog.askstring("Input", "Enter new instruction:")
        if new_instruction and UVSim.is_valid_instruction(new_instruction):
            self.program_text.insert(tk.END, f"{new_instruction}\n")
            self.program = [int(line) for line in self.program_text.get(1.0, tk.END).strip().split("\n")]

    def delete_instruction(self):
        try:
            start_index = self.program_text.index(tk.SEL_FIRST)
            end_index = self.program_text.index(tk.SEL_LAST)
            self.program_text.delete(start_index, end_index)
            self.program = [int(line) for line in self.program_text.get(1.0, tk.END).strip().split("\n")]
        except tk.TclError:
            messagebox.showerror("Error", "Please select the instruction to delete.")

    def display_program(self, program):
        current_tab = self.notebook.select()
        file_path = self.notebook.tab(current_tab, "text")
        self.programs[file_path].delete(1.0, tk.END)
        for instruction in program:
            self.programs[file_path].insert(tk.END, f"{instruction:06}\n")

    def display_memory(self):
        for i in self.memory_tree.get_children():
            self.memory_tree.delete(i)
        for address, value in enumerate(self.uvsim.memory):
            self.memory_tree.insert("", tk.END, values=(address, value))

    def run_program(self):
        self.output_text.delete(1.0, tk.END)
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
        self.output_text.insert(tk.END, f"{message}\n")

    def update_status(self):
        self.accumulator_label.config(text=f"Accumulator: [{self.uvsim.accumulator:06}]")
        self.pc_label.config(text=f"Program Counter: [{self.uvsim.pc:06}]")
        self.display_memory()


def main():
    root = tk.Tk()
    app = UVSimGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
