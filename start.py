import tkinter as tk


class UVSim:
    def __init__(self):
        self.memory = [0] * 100
        self.accumulator = 0
        self.pc = 0
        self.running = True
        self.waiting_for_input = False
        self.gui = None

    def set_gui(self, gui):
        self.gui = gui

    def load_program(self, program):
        self.memory = [0] * 100
        for i, instruction in enumerate(program):
            self.memory[i] = instruction
        self.accumulator = 0
        self.pc = 0
        self.running = True

    def fetch(self):
        if not self.running:
            return None
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction

    def decode_execute(self, instruction):
        if not self.running:
            return
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
                if instruction is not None:
                    self.decode_execute(instruction)
                    if self.gui:
                        self.gui.update_status()

    def set_status(self, message):
        if self.gui:
            self.gui.set_status(message)

    def display_output(self, message):
        if self.gui:
            self.gui.display_message(message)

    def request_input(self, prompt, callback):
        if self.gui:
            self.gui.request_input(prompt, callback)

    @staticmethod
    def is_valid_instruction(instruction):
        if (instruction.startswith('+') or instruction.startswith('-')) and len(instruction) == 5:
            try:
                int(instruction)
                return True
            except ValueError:
                return False
        elif len(instruction) == 4:
            try:
                int(instruction)
                return True
            except ValueError:
                return False
        return False

    def check_overflow(self, value):
        max_val = 9999
        min_val = -9999
        if value > max_val:
            return value % 10000
        elif value < min_val:
            return -((-value) % 10000)
        return value


class Operation:
    def __init__(self, sim, operand):
        self.sim = sim
        self.operand = operand

    def execute(self):
        raise NotImplementedError("This method should be overridden by subclasses")


class Read(Operation):
    def execute(self):
        self.sim.waiting_for_input = True
        self.sim.request_input(f"Enter an integer for memory location {self.operand}:", self.handle_input)

    def handle_input(self, value):
        try:
            value = int(value)
            self.sim.memory[self.operand] = value
            self.sim.waiting_for_input = False
        except ValueError:
            self.sim.set_status("Invalid input. Please enter a valid integer.")
            self.sim.waiting_for_input = True
            self.sim.request_input(f"Enter an integer for memory location {self.operand}:", self.handle_input)


class Write(Operation):
    def execute(self):
        message = f"Value at memory location {self.operand}: {self.sim.memory[self.operand]}"
        self.sim.display_output(message)


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
            message = "Error: Division by zero"
            self.sim.set_status(message)
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
        message = "Halting execution"
        self.sim.set_status(message)
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


if __name__ == "__main__":
    import gui
    gui.main()
