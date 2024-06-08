import unittest
from io import StringIO
import sys
from start import UVSim

class TestUVSim(unittest.TestCase):
    def setUp(self):
        self.uvsim = UVSim()

    def test_read_success(self):
        program = [1001, 4300]
        self.uvsim.load_program(program)
        original_stdin = sys.stdin
        sys.stdin = StringIO('1001\n')
        self.uvsim.run()
        self.assertEqual(self.uvsim.memory[1], 1001)
        sys.stdin = original_stdin

    def test_write_success(self):
        program = [1100, 4300]
        self.uvsim.load_program(program)
        self.uvsim.memory[0] = 1234
        output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        self.uvsim.run()
        self.assertIn('1234', output.getvalue())
        sys.stdout = original_stdout

    def test_load_success(self):
        program = [2000, 4300]
        self.uvsim.memory[0] = 2000
        self.uvsim.load_program(program)
        self.uvsim.run()
        self.assertEqual(self.uvsim.accumulator, 2000)

    def test_store_success(self):
        program = [2100, 4300]
        self.uvsim.accumulator = 1234
        self.uvsim.load_program(program)
        self.uvsim.run()
        self.assertEqual(self.uvsim.memory[0], 1234)

    def test_add_success(self):
        program = [2000, 3001, 4300]
        self.uvsim.memory[0] = 1723
        self.uvsim.memory[1] = 3001
        self.uvsim.load_program(program)
        self.uvsim.run()
        self.assertEqual(self.uvsim.accumulator, 5001)

    def test_subtract_success(self):
        program = [1000,1001, 2001, 3100, 4300]
        self.uvsim.load_program(program)
        self.uvsim.run()
        self.assertEqual(self.uvsim.accumulator, 1)

    def test_divide_success(self):
        program = [1000, 2000, 3200, 4300]
        self.uvsim.load_program(program)
        self.uvsim.run()
        self.assertEqual(self.uvsim.accumulator, 1)

    def test_multiply_success(self):
        program = [1000, 2000, 3300, 4300]
        self.uvsim.load_program(program)
        self.uvsim.run()
        self.assertEqual(self.uvsim.accumulator, 1000000)

    def test_branch_success(self):
        program = [4001, 1101, 4300]
        self.uvsim.load_program(program)
        self.uvsim.memory[1] = 5678
        output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        self.uvsim.run()
        self.assertIn('5678', output.getvalue())
        sys.stdout = original_stdout

    def test_branchneg_success(self):
        program = [2000, 4102, 1102, 4300]
        self.uvsim.memory[0] = -1
        self.uvsim.memory[2] = 9999
        self.uvsim.load_program(program)
        output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        self.uvsim.run()
        self.assertIn('9999', output.getvalue())
        sys.stdout = original_stdout

    def test_branchzero_success(self):
        program = [2000, 4202, 1102, 4300]
        self.uvsim.memory[0] = 0
        self.uvsim.memory[2] = 9999
        self.uvsim.load_program(program)
        output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        self.uvsim.run()
        self.assertIn('9999', output.getvalue())
        sys.stdout = original_stdout

    def test_halt_success(self):
        program = [4300]
        self.uvsim.load_program(program)
        self.uvsim.run()
        self.assertFalse(self.uvsim.running)

if __name__ == "__main__":
    unittest.main()
