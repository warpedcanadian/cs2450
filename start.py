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
        class_id_dict = {
            10: Read, 
            11: Write, 
            20: Load, 
            21: Store, 
            30: Add, 
            31: Subtract, 
            32 :Divide, 
            33: Multiply, 
            40: Branch, 
            41: BranchNeg, 
            42: BranchZero, 
            43: Halt 
        }
        
        for key, value in class_id_dict:
            opcode = key
            if opcode in class_id_dict:
                class_id_dict[opcode](value)
        if opcode == 10:  # READ
            value = int(input(f"Enter an integer for memory location {operand}: "))
            self.memory[operand] = value

        elif opcode == 11:  # WRITE
            print(self.memory[operand])

        elif opcode == 20:  # LOAD
            self.accumulator = self.memory[operand]

        elif opcode == 21:  # STORE
            self.memory[operand] = self.accumulator

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

class Read(UVSim):
    pass
class Write(UVSim):
    pass
class Load(UVSim):
    pass
class Store(UVSim):
    pass
class Add(UVSim):
    pass
class Subtract(UVSim):
    pass
class Multiply(UVSim):
    pass
class Divide(UVSim):
    pass
class Branch(UVSim):
    def __init__(self, operand):
        super().__init__()
        self.pc = operand

class BranchNeg(UVSim):
     def __init__(self, operand):
        super().__init__()
        if self.accumulator < 0:
            self.pc = operand
        return self.pc
class BranchZero(UVSim):
     def __init__(self, operand): 
        super().__init__()           
        if self.accumulator == 0:
            self.pc = operand
        return self.pc
class Halt(UVSim):
     def __init__(self):
        super().__init__()
        print("Halting execution")
        self.running = False
        return self.running
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
