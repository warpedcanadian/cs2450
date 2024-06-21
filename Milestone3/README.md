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
- tkinter library (included by default with Python installations).

Installation
-------------
1. Download or clone the repository containing start.py, gui.py, and the example program file.
2. Ensure all files are in the same directory.
   
Usage Instructions
------------------
1. Save the start.py and gui.py files (provided in the project) to a directory on your computer.
2. Create a BasicML program file (e.g., Test1.txt) with each instruction on a new line.
3. Open a command line terminal and navigate to the directory containing `start.py`.
4. Run the UVSim program with the following command: `python start.py`
Note: Only valid four-digit instructions (with optional sign) will be accepted. Invalid instructions will be ignored with a warning message.

Using the GUI
------------------
1. Opening the Application:
  -Running the start.py script will launch the GUI for the UVSim.

2. GUI Controls:
  - File:
    - Open: Open a .txt file containing the BasicML program.
    - Exit: Exit the application.
  
  - Help:
    - About: Display information about the application.
  
  - Toolbar:
    - Open File: Open a .txt file containing the BasicML program. This will load the program into the simulator.
    - Run: Execute the loaded BasicML program.
    - Stop: Stop the execution of the program.

  - Program Instructions Panel:
    - Displays the loaded BasicML program instructions. Each line represents an instruction in the program.
    - Memory Display Panel:
    - Columns:
      - Address: The memory address.
      - Value: The value stored at the memory address.
    -Displays the current state of the simulator's memory.
  
  - Status Panel:
    - Accumulator: Shows the current value of the accumulator.
    - Program Counter: Shows the current value of the program counter.
    - Status: Shows the current status of the simulator (e.g., Ready, Running, Stopped)

3. Workflow:
  - Loading a Program:
    - Click on Open File from the toolbar or File > Open from the menu bar.
    - Select a .txt file containing the BasicML program. The program instructions will be displayed in the Program Instructions panel.

  - Running the Program:
    - Click on Run from the toolbar to start executing the loaded program.
    - The simulator will execute the instructions, and the memory display and status panel will be updated accordingly.
   
   - Stopping the Program:
    - Click on Stop from the toolbar to halt the execution of the program.

4. Handling Input:
  - During the execution, if a READ instruction is encountered, an input dialog will       
    appear asking for an integer input. Enter the value and press Enter or click Submit.      

Unit Testing
------------
To run the unit tests, save the test script (`unit_tests.py`) to the same directory as `start.py`. Run the tests using the following command: `python unit_tests.py`

This will execute all the unit tests and display the results in the terminal.
