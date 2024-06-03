# cs2450
Software Engineering Group Project

UVSim Simulator
===============

Description
-----------
UVSim is a simple virtual machine designed to help computer science students learn machine language and computer architecture. It interprets a machine language called BasicML, allowing students to execute their machine language programs on the simulator.

Prerequisites
-------------
- Python 3.x installed on your system.
- BasicML program file (a text file with instructions).

Usage Instructions
------------------
1. Save the `uvsim.py` file (provided in the project) to a directory on your computer.
2. Create a BasicML program file (e.g., `program.txt`) with each instruction on a new line.
3. Open a command line terminal and navigate to the directory containing `uvsim.py`.
4. Run the UVSim program with the following command:
5. When prompted, enter the name of the BasicML program file (e.g., `program.txt`). If the file is not found, you will be prompted to try again until a valid file is provided.
6. Follow the on-screen prompts for input (if the program includes READ instructions) and observe the outputs.

Note: Only valid four-digit instructions (with optional sign) will be accepted. Invalid instructions will be ignored with a warning message. For `READ` operations, only valid four-digit numbers with an optional sign will be accepted as input.

Unit Testing
------------
To run the unit tests, save the test script (`test_uvsim.py`) to the same directory as `uvsim.py`. Run the tests using the following command:

This will execute all the unit tests and display the results in the terminal.