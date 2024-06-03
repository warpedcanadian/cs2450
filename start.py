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
            self.memory[operand] = int(input("Enter a number: "))
        elif opcode == 11:  # WRITE
            print(self.memory[operand])

        # Load/Store operators go here...probably.

        # Arithmetic operators go here...probably.

        # Control operators go here...probably.

        elif opcode == 43:  # HALT
            self.running = False

    def run(self):
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)


def load_program_from_file(filename):
    program = []
    with open(filename, 'r') as file:
        for line in file:
            program.append(int(line.strip()))
    return program


def main():
    filename = input("Enter the program file name (ex. Test1.txt): ")
    program = load_program_from_file(filename)

    uvsim = UVSim()
    uvsim.load_program(program)
    uvsim.run()


if __name__ == "__main__":
    main()
