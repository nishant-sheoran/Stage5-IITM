# RISC-V 5-Stage Pipelined Simulator

This project is a Python-based simulator for the RISC-V instruction set, supporting both single-stage and 5-stage pipelined architectures. It is designed for educational and experimental purposes, focusing on basic arithmetic and logical operations, hazard detection, and pipeline visualization.

## Features
- **5-Stage Pipeline Simulation:** Models IF, ID, EX, MEM, WB stages with hazard detection and forwarding.
- **Single-Stage Simulation:** For comparison and reference.
- **Graphical User Interface (GUI):** Built with Tkinter for easy visualization and control.
- **Performance Metrics:** Automatically calculates and displays cycles, instructions, CPI, and IPC at the end of simulation.
- **Flexible Input/Output:** Accepts custom input files and generates detailed output for registers, memory, and pipeline state.

## Schematic

### Single Stage

![Schematic RISCV Project Single Stage.png](docs/Schematic%20RISCV%20Project%20Single%20Stage.png)
Schematic modified from [Textbook](##Reference) Figure 4.25

**Description:**

The simulator was designed to follow the Simple Implementation Scheme from the textbook Computer Organization and Design RISC-V Edition 2nd. To utilize the pipeline and the State class, I implemented the pipeline registers and Pipelined Control mentioned in Chapter 4.7.
However, the BNE and JAL instructions are not achievable with the Simple Implementation Scheme. So, compared to the single stage datapath from the textbook Figure 4.25, I made the following changes to complete the functionality:
- added 2 control signals (ALUSrcA, JAL)
- added 1 MUX (ALU input A)
- added 2 gates (XOR, OR)
- modified a MUX (ALU input B)
- connected PC to a MUX(ALU input A) and instruction[12] to the XOR gate.

### Five Stage

![Schematic RISCV Project Five Stage.png](docs/Schematic%20RISCV%20Project%20Five%20Stage.png)
Modified from [Textbook](##Reference) Figure 4.62

**Description:**

In the Five-Stage machine, I added the forwarding unit and the hazard control unit to solve hazards introduced in the Mulit-stage pipeline. I kept the design of the control unit and PCSrc (from the result of 3 logic gates) and significantly modified other parts of the branch condition  by moving it from the EX stage to the ID stage. Additionally, I implemented a dedicated forwarding unit to handle branch decision input choices.

## How to Use

### 1. **Running the GUI**
- Make sure you have Python 3 and all dependencies installed (`pip install -r requirements.txt`).
- Run the GUI:
  ```bash
  python pipeline_gui.py
  ```
- Use the GUI to:
  - Load a folder containing `imem.txt` (instruction memory) and `dmem.txt` (data memory).
  - Step through the simulation cycle by cycle.
  - Visualize the pipeline stages and see the current state.
  - At the end, view performance metrics in a popup.

### 2. **Input Files**
- `imem.txt`: Each line is 8 bits (one byte) in binary, representing the instruction memory.
- `dmem.txt`: Each line is 8 bits (one byte) in binary, representing the data memory.
- Place both files in the same folder and select either one when loading input in the GUI.

### 3. **Output Files**
- `FS_/RFResult.txt`: Register file state after each cycle (FS mode).
- `StateResult_FS.txt`: Pipeline state after each cycle (FS mode).
- `FS_DMEMResult.txt`: Data memory after simulation (FS mode, if enabled).
- `PerformanceMetrics_Result.txt`: Performance metrics (cycles, instructions, CPI, IPC).
- Other files may be generated for single-stage mode or for reference.

### 4. **Performance Metrics**
- At the end of simulation, the GUI will display:
  - Number of cycles taken
  - Total number of instructions
  - Cycles per instruction (CPI)
  - Instructions per cycle (IPC)
- These are also saved to `PerformanceMetrics_Result.txt` in your input/output folder.

## Project Structure
- `pipeline_gui.py`: Main GUI for running and visualizing the simulator.
- `src/`: Source code for the simulator core, memory, register file, hazard handling, and metrics.
- `input/`: Example input files (`imem.txt`, `dmem.txt`, `Code.asm`).
- `Sample_Testcases_FS/`: Sample testcases with input and reference output files.
- `docs/`: Schematics and documentation.

## Reference

All references came from:
Computer Organization and Design RISC-V Edition 2nd ED 2021 by **David A. Patterson & John L. Hennessy** 

## License

This repo is licensed under the MIT License