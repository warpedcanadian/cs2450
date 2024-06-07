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

        if opcode == 10:  # READ
            while True:
                user_input = input("Enter a four-digit number (ex. +1234, -5678): ")
                if self.is_valid_instruction(user_input):
                    self.memory[operand] = int(user_input)
                    break
                else:
                    print("Invalid input. Please enter a valid four-digit number with an optional sign.")
        elif opcode == 11:  # WRITE
            print(self.memory[operand])

        elif opcode == 20:  # Load
            self.accumulator = operand

        elif opcode == 21:  # Store
            operand = self.accumulator

        elif opcode == 30:  # ADD
            self.accumulator += self.memory[operand]
        elif opcode == 31:  # SUBTRACT
            self.accumulator -= self.memory[operand]
        elif opcode == 32:  # DIVIDE
            if self.memory[operand] == 0:
                print("Error: Division by zero")
                self.running = False
            else:
                self.accumulator //= self.memory[operand]
        elif opcode == 33:  # MULTIPLY
            self.accumulator *= self.memory[operand]


        elif opcode == 40: #BRANCH
            self.pc = self.memory[operand]

        elif opcode == 41: #BRANCHNEG
            if self.accumulator < 0:
                self.pc = self.memory[operand]
        
        elif opcode == 42: #BRANCHZERO
            if self.accumulator == 0:
                self.pc = self.memory[operand]
                
        elif opcode == 43:  # HALT
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
