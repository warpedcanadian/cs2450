class UVSim:
    def __init__(self):
        self.memory = [0] * 100
        self.accumulator = 0
        self.pc = 0
        self.running = True

    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

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

    def run(self):
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)

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
            return max_val
        elif value < min_val:
            return min_val
        return value


class Operation:
    def __init__(self, sim, operand):
        self.sim = sim
        self.operand = operand

    def execute(self):
        raise NotImplementedError("This method should be overridden by subclasses")


class Read(Operation):
    def execute(self):
        value = int(input(f"Enter an integer for memory location {self.operand}: "))
        self.sim.memory[self.operand] = value


class Write(Operation):
    def execute(self):
        print(self.sim.memory[self.operand])


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
    while True:
        try:
            filename = input("Enter the program file name (ex. Test1.txt): ")
            program = load_program_from_file(filename)
            if not program:
                raise ValueError("No valid instructions found in the file.")
            break
        except FileNotFoundError:
            print(f"File '{filename}' not found. Please try again.")
        except ValueError as e:
            print(e)

    uvsim = UVSim()
    uvsim.load_program(program)
    uvsim.run()


if __name__ == "__main__":
    main()
