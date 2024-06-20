import gui
import os
import sys
import subprocess

class UVSim:
    def __init__(self, raw_data):
        self.memory = [None] * 100
        self.accumulator = 0
        self.pc = 0
        self.running = True
        self.raw_data = raw_data
        
        print(raw_data)
        for i, instruction in enumerate(raw_data):
            self.memory[i] = instruction

    def fetch(self):
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction

    def decode_execute(self, instruction):
        opcode = instruction // 100
        operand = instruction % 100
        class_id_dict = {
            10: Read(operand), 
            11: Write(operand), 
            20: Load(operand), 
            21: Store(operand), 
            30: Add(operand), 
            31: Subtract(operand), 
            32 :Divide(operand), 
            33: Multiply(operand), 
            40: Branch(operand), 
            41: BranchNeg(operand), 
            42: BranchZero(operand), 
            43: Halt(operand) 
        }
        
        for opcode, value in class_id_dict.items():
            if not opcode in class_id_dict:
                raise ValueError('Invalid opcode')
            else:
                class_id_dict[opcode](value)
        '''        
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
        '''
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
    def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        value = int(input(f"Enter an integer for memory location {operand}: "))
        self.memory[operand] = value
class Write(UVSim):
     def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        print(self.memory[operand])

class Load(UVSim):
    def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        self.accumulator = self.memory[operand]
class Store(UVSim):
    def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        self.memory[operand] = self.accumulator
class Add(UVSim):
    def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        if self.memory[operand] == None:
            print('Nothing to add')
            return
        else:
            self.accumulator += self.memory[operand]
class Subtract(UVSim):
    def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        if self.memory[operand] == None:
            print('Nothing to subtract')
        else:
            self.accumulator -= self.memory[operand]
class Multiply(UVSim):
    def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        if self.memory[operand] == None:
            print('Nothing to multiply by')
            return
        else:
            self.accumulator *= self.memory[operand]
class Divide(UVSim):
    def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        if self.memory[operand] == 0:
            print("Error: Division by zero")
            self.running = False
        elif self.memory[operand] == None:
            print('Nothing to divide by')
            return
        else:
            self.accumulator /= self.memory[operand] 
class Branch(UVSim):
    def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        self.pc = operand

class BranchNeg(UVSim):
     def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        if self.accumulator < 0:
            self.pc = operand
        return self.pc
class BranchZero(UVSim):
     def __init__(self, raw_data, operand):
        super().__init__(raw_data)         
        if self.accumulator == 0:
            self.pc = operand
        return self.pc
class Halt(UVSim):
     def __init__(self, raw_data, operand):
        super().__init__(raw_data)
        print("Halting execution")
        self.running = False
        return self.running
     
def main():
    get_file = gui.file_open()   
    uvsim = UVSim(get_file)
    #uvsim.load_program(get_file)
    gui.window.mainloop()
    while True:
        uvsim.run()   
        
if __name__ == "__main__":
    main()
