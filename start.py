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
        print(f"Executing instruction: {instruction} (PC: {self.pc}, ACC: {self.accumulator})")

        if opcode == 10:  # READ
            value = int(input(f"Enter an integer for memory location {operand}: "))
            self.memory[operand] = value

        elif opcode == 11:  # WRITE
            print(f"Output from memory[{operand}]: {self.memory[operand]}")
            print(self.memory[operand])

        elif opcode == 20:  # LOAD
            self.accumulator = self.memory[operand]
            print(f"Loaded {self.accumulator} into accumulator from memory[{operand}]")

        elif opcode == 21:  # STORE
            self.memory[operand] = self.accumulator
            print(f"Stored {self.accumulator} from accumulator into memory[{operand}]")

        elif opcode == 30:  # ADD
            self.accumulator += self.memory[operand]
            print(f"Added {self.memory[operand]} to accumulator, new value: {self.accumulator}")

        elif opcode == 31:  # SUBTRACT
            self.accumulator -= self.memory[operand]
            print(f"Subtracted {self.memory[operand]} from accumulator, new value: {self.accumulator}")

        elif opcode == 32:  # DIVIDE
            if self.memory[operand] == 0:
                print("Error: Division by zero")
                self.running = False
            else:
                self.accumulator //= self.memory[operand]
                print(f"Divided accumulator by {self.memory[operand]}, new value: {self.accumulator}")

        elif opcode == 33:  # MULTIPLY
            self.accumulator *= self.memory[operand]
            print(f"Multiplied accumulator by {self.memory[operand]}, new value: {self.accumulator}")

        elif opcode == 40:  # BRANCH
            self.pc = operand
            print(f"Branched to address {operand}")

        elif opcode == 41:  # BRANCHNEG
            if self.accumulator < 0:
                self.pc = operand
                print(f"Branched to address {operand} because accumulator is negative")

        elif opcode == 42:  # BRANCHZERO
            if self.accumulator == 0:
                self.pc = operand
                print(f"Branched to address {operand} because accumulator is zero")

        elif opcode == 43:  # HALT
            print("Halting execution")
            self.running = False

    def run(self):
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)

    def is_valid_instruction(self, instruction):
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

def load_program_from_file(filename):
    program = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if UVSim().is_valid_instruction(line):
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
