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
1. Save the `start.py`, `gui.py`, and `refactor.py` files (provided in the project) to a directory on your computer.
2. Create a BasicML program file (e.g., `Test1.txt`) with each instruction on a new line.
3. Open a command line terminal and navigate to the directory containing `start.py`.
4. Run the UVSim program with the following command: `python start.py`
5. The GUI will launch. Use the `File` menu to open a BasicML program file (e.g., `Test1.txt`). If the file is not found, you will be prompted to try again until a valid file is provided.
6. You can run, add, delete instructions, and change the color scheme using the GUI.
7. Follow the on-screen prompts for input (if any) and observe the outputs in the GUI.

Note: 

- Only valid instructions (either 4-digit or 6-digit with optional sign) will be accepted. Invalid instructions will be ignored with a warning message.
- Opening a second file will create another tab in the left pane where the program instructions are located. You can click back and forth and operate their own instances.

Features
--------
- **Graphical User Interface (GUI):** Allows for easy interaction with the simulator, including loading, running, and saving programs.
- **Memory Display:** Visual representation of memory content.
- **Status Display:** Shows the current status of the accumulator, program counter, and execution status.
- **Color Scheme Customization:** Users can change the primary and off colors of the GUI.
- **Instruction Conversion:** Convert 4-digit instructions to 6-digit format through the GUI.

File Descriptions
-----------------
- `start.py`: Contains the core logic of the UVSim simulator, including memory management, instruction fetching, decoding, and execution.
- `gui.py`: Implements the graphical user interface for the UVSim simulator, providing functionalities for file operations, program execution, and user interactions.
- `refactor.py`: An alternative GUI implementation focusing on refactoring and modular design.
- `config.json`: Stores the color scheme settings for the GUI.

Menu and Button Descriptions
----------------------------
### File Menu
- **Open:** Opens a file dialog to select a BasicML program file to load into the simulator. The program instructions are displayed in a new tab in the GUI.
- **Save:** Saves the current program instructions back to the file from which they were loaded.
- **Convert to 6-Digit:** Converts the instructions in a selected file from 4-digit format to 6-digit format and saves the converted instructions to a new file.
- **Exit:** Closes the simulator.

### Edit Menu
- **Add Instruction:** Prompts the user to enter a new instruction, which is then added to the current program.
- **Delete Instruction:** Deletes the selected instruction from the current program.
- **Change Color Scheme:** Opens a color chooser dialog to change the primary and off colors of the GUI. The selected colors are saved to `config.json`.

### Help Menu
- **About:** Displays information about the UVSim simulator.

### Toolbar Buttons
- **Run:** Runs the loaded program in the simulator. The program's execution status, accumulator, and memory contents are updated in the GUI.
- **Save:** Saves the current program instructions back to the file from which they were loaded.

Unit Testing
------------
To run the unit tests, save the test script (`unit_tests.py`) to the same directory as `start.py`. Run the tests using the following command: `python unit_tests.py`

This will execute all the unit tests and display the results in the terminal.

Please make sure all files are in the same directory for the simulator to function correctly.
