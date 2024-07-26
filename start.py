import tkinter as tk
from tkinter import messagebox

class UVSim:
    def __init__(self):
        self.memory = [0] * 250  # Change memory size to 250
        self.accumulator = 0
        self.pc = 0
        self.running = True
        self.waiting_for_input = False
        self.gui = None

    def set_gui(self, gui):
        self.gui = gui

    def load_program(self, program):
        self.memory = [0] * 250  # Change memory size to 250
        for i, instruction in enumerate(program):
            if i < len(self.memory):
                self.memory[i] = instruction
        self.accumulator = 0
        self.pc = 0
        self.running = True

    def fetch(self):
        if not self.running:
            return 0  # Return a noop if not running to avoid out of bounds
        if self.pc < len(self.memory):
            instruction = self.memory[self.pc]
            print(f"Fetching instruction at PC={self.pc}: {instruction}")
            self.pc += 1
            return instruction
        else:
            self.running = False
            raise IndexError("Program Counter exceeded memory bounds.")

    def decode_execute(self, instruction):
        opcode = (instruction // 1000) % 1000  # Extracting the three-digit opcode
        operand = instruction % 1000  # Extracting the three-digit operand
        print(f"Decoding instruction: opcode={opcode:03d}, operand={operand:03d}")
        operation_classes = {
            10: Read,
            11: Write,
            20: Load,
            21: Store,
            30: Add,
            31: Subtract,
            32: Divide,
            33: Multiply,
            40: Branch,
            41: BranchNeg,
            42: BranchZero,
            43: Halt
        }

        if opcode in operation_classes:
            operation = operation_classes[opcode](self, operand)
            operation.execute()
        else:
            self.running = False  # Stop the simulation if the instruction is invalid
        if self.gui:
            self.gui.display_memory()

    def run(self):
        while self.running:
            if not self.waiting_for_input:
                try:
                    instruction = self.fetch()
                    self.decode_execute(instruction)
                    if not self.running:
                        break
                except IndexError as e:
                    self.running = False
                    if self.gui:
                        self.gui.display_message(str(e))
                    break
            if self.gui:
                self.gui.update_status()
        print(f"Program halted. Final PC={self.pc}, Accumulator={self.accumulator}")

    @staticmethod
    def is_valid_instruction(instruction):
        # Check for six-digit instructions with a sign
        if len(instruction) == 7 and (instruction[0] == '+' or instruction[0] == '-'):
            try:
                int(instruction[1:])  # Ensure the rest is numeric
                return True
            except ValueError:
                return False
        # Check for five-digit instructions with a sign
        elif len(instruction) == 5 and (instruction[0] == '+' or instruction[0] == '-'):
            try:
                int(instruction)
                return True
            except ValueError:
                return False
        return False

    def check_overflow(self, value):
        max_val = 999999
        min_val = -999999
        if value > max_val:
            return value % (max_val + 1)
        elif value < min_val:
            return -(abs(value) % (max_val + 1))
        return value

class Operation:
    def __init__(self, sim, operand):
        self.sim = sim
        self.operand = operand

    def execute(self):
        raise NotImplementedError("This method should be overridden by subclasses")

class Read(Operation):
    def execute(self):
        if self.sim.gui:
            self.sim.waiting_for_input = True
            input_dialog = tk.Toplevel(self.sim.gui.root)
            input_dialog.title("Input")
            tk.Label(input_dialog, text=f"Enter an integer for memory location {self.operand}:").pack()
            input_var = tk.IntVar()

            def on_submit(event=None):
                try:
                    value = int(entry.get())
                    input_var.set(value)
                    input_dialog.destroy()
                except ValueError:
                    messagebox.showerror("Invalid input", "Please enter a valid integer.")

            entry = tk.Entry(input_dialog)
            entry.pack()
            entry.bind("<Return>", on_submit)
            tk.Button(input_dialog, text="Submit", command=on_submit).pack()
            input_dialog.transient(self.sim.gui.root)
            input_dialog.grab_set()
            input_dialog.geometry(f"+{self.sim.gui.root.winfo_rootx() + self.sim.gui.root.winfo_width() // 2 - input_dialog.winfo_reqwidth() // 2}+{self.sim.gui.root.winfo_rooty() + self.sim.gui.root.winfo_height() // 2 - input_dialog.winfo_reqheight() // 2}")
            self.sim.gui.root.wait_window(input_dialog)

            value = input_var.get()
            self.sim.memory[self.operand] = value
            self.sim.waiting_for_input = False
        else:
            value = int(input(f"Enter an integer for memory location {self.operand}: "))
            self.sim.memory[self.operand] = value

class Write(Operation):
    def execute(self):
        print(self.sim.memory[self.operand])
        if self.sim.gui:
            self.sim.gui.display_message(f"Value at memory location {self.operand}: {self.sim.memory[self.operand]}")

class Load(Operation):
    def execute(self):
        self.sim.accumulator = self.sim.memory[self.operand]

class Store(Operation):
    def execute(self):
        self.sim.memory[self.operand] = self.sim.accumulator

class Add(Operation):
    def execute(self):
        self.sim.accumulator += self.sim.memory[self.operand]
        self.sim.accumulator = self.sim.check_overflow(self.sim.accumulator)

class Subtract(Operation):
    def execute(self):
        self.sim.accumulator -= self.sim.memory[self.operand]
        self.sim.accumulator = self.sim.check_overflow(self.sim.accumulator)

class Multiply(Operation):
    def execute(self):
        self.sim.accumulator *= self.sim.memory[self.operand]
        self.sim.accumulator = self.sim.check_overflow(self.sim.accumulator)

class Divide(Operation):
    def execute(self):
        if self.sim.memory[self.operand] == 0:
            print("Error: Division by zero")
            if self.sim.gui:
                self.sim.gui.display_message("Error: Division by zero")
            self.sim.running = False
        else:
            self.sim.accumulator //= self.sim.memory[self.operand]
            self.sim.accumulator = self.sim.check_overflow(self.sim.accumulator)

class Branch(Operation):
    def execute(self):
        self.sim.pc = self.operand

class BranchNeg(Operation):
    def execute(self):
        if self.sim.accumulator < 0:
            self.sim.pc = self.operand

class BranchZero(Operation):
    def execute(self):
        if self.sim.accumulator == 0:
            self.sim.pc = self.operand

class Halt(Operation):
    def execute(self):
        print("Halting execution")
        if self.sim.gui:
            self.sim.gui.display_message("Halting execution")
        self.sim.running = False

def load_program_from_file(filename):
    program = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            print(f"Reading line: {line}")  # Debugging statement
            if line:
                if UVSim.is_valid_instruction(line):
                    # Ensure instruction is converted to a six-digit format
                    program.append(int(line))
                else:
                    print(f"Invalid instruction '{line}' ignored.")
    print(f"Loaded program: {program}")  # Debugging statement
    return program


if __name__ == "__main__":
    import gui
    gui.main()
