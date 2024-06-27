import tkinter as tk
from tkinter import messagebox
from gui import UVSimGUI

class UVSim:
    def __init__(self, gui):
        self.memory = [0] * 100
        self.accumulator = 0
        self.pc = 0
        self.running = True
        self.waiting_for_input = False
        self.gui = gui

    #def set_gui(self, gui):
        #self.gui = gui

    def load_program(self, program):
        self.memory = [0] * 100
        for i, instruction in enumerate(program):
            self.memory[i] = instruction
        self.accumulator = 0
        self.pc = 0
        self.running = True

    def fetch(self):
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction

    def decode_execute(self, instruction):
        opcode = instruction // 100
        operand = instruction % 100
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
        if self.gui:
            self.gui.display_memory()

    def run(self):
        while self.running:
            if not self.waiting_for_input:
                instruction = self.fetch()
                self.decode_execute(instruction)
                if self.gui:
                    self.gui.update_status()

    @staticmethod
    def is_valid_instruction(instruction):
        if (instruction.startswith('+') or instruction.startswith('-')) and len(instruction) > 4:
            new_instruction = instruction[-4:-1]
            return new_instruction
        elif len(instruction) == 4:
            try:
                int(instruction)
                return True
            except ValueError:
                return False
        return False

    #def check_overflow(self, value):
        #if len(value) > 4:
           # new_value = value[-4:-1]
        #return new_value

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
            if line:
                if UVSim.is_valid_instruction(line):
                    program.append(int(line))
                else:
                    print(f"Invalid instruction '{line}' ignored.")
    return program

def main():
 root = tk.Tk()
 interface = UVSimGUI(root)
 app = UVSim()
 load_program_from_file()
 app.load_program()
 app.fetch()
 root.mainloop()

if __name__ == "__main__":
    import gui
    gui.main()
