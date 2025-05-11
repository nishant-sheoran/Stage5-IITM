import tkinter as tk
from tkinter import filedialog, messagebox
from src.core import FiveStageCore
from src.memory import InstructionMemory, DataMemory
from src.generate_metrics import generate_metrics
from pathlib import Path

class PipelineGUI:
    def __init__(self, master):
        self.master = master
        master.title("RISC-V 5-Stage Pipeline Simulator")

        self.core = None
        self.cycle = 0
        self.pipeline_labels = []
        self.total_instructions = 0  # Track total instructions for metrics

        # Controls
        self.load_button = tk.Button(master, text="Load Input File", command=self.load_file)
        self.load_button.pack(pady=5)

        self.step_button = tk.Button(master, text="Next Cycle", command=self.next_cycle, state=tk.DISABLED)
        self.step_button.pack(pady=5)

        # Pipeline Table
        self.table_frame = tk.Frame(master)
        self.table_frame.pack(pady=10)
        self.stage_names = ["IF", "ID", "EX", "MEM", "WB"]
        self.stage_labels = []
        for i, stage in enumerate(self.stage_names):
            lbl = tk.Label(self.table_frame, text=stage, borderwidth=2, relief="groove", width=15)
            lbl.grid(row=0, column=i)
            self.stage_labels.append(lbl)
        self.value_labels = []
        for i in range(len(self.stage_names)):
            val_lbl = tk.Label(self.table_frame, text="-", borderwidth=2, relief="sunken", width=15)
            val_lbl.grid(row=1, column=i)
            self.value_labels.append(val_lbl)

        # Cycle label
        self.cycle_label = tk.Label(master, text="Cycle: 0")
        self.cycle_label.pack(pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path:
            return
        try:
            io_dir = Path(file_path).parent
            instruction_memory = InstructionMemory("imem", io_dir)
            data_memory = DataMemory("dmem", io_dir)
            self.core = FiveStageCore(io_dir, instruction_memory, data_memory)
            self.cycle = 0
            self.total_instructions = 0
            self.update_table()
            self.step_button.config(state=tk.NORMAL)
            self.cycle_label.config(text=f"Cycle: {self.cycle}")
            messagebox.showinfo("Loaded", f"Loaded input file: {file_path}\nMake sure this folder contains both imem.txt and dmem.txt.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def next_cycle(self):
        if not self.core or self.core.halted:
            self.step_button.config(state=tk.DISABLED)
            return
        # Count non-NOP instructions entering WB stage
        wb_stage = self.core.state.WB
        if not wb_stage.get("nop", True):
            self.total_instructions += 1
        self.core.step()
        self.cycle += 1
        self.update_table()
        self.cycle_label.config(text=f"Cycle: {self.cycle}")
        if self.core.halted:
            self.step_button.config(state=tk.DISABLED)
            self.show_performance_metrics()
            messagebox.showinfo("Halted", "Simulation halted.")

    def show_performance_metrics(self):
        # Generate and display performance metrics
        io_dir = self.core.ioDir.parent if hasattr(self.core, 'ioDir') else Path('.')
        head_cont = "Performance Metrics for RISC-V 5-Stage Pipeline"
        cycles = self.cycle
        tot_ins = self.total_instructions if self.total_instructions > 0 else 1
        generate_metrics("w", head_cont, cycles, tot_ins, io_dir)
        metrics_path = io_dir / "PerformanceMetrics_Result.txt"
        try:
            with open(metrics_path, "r") as f:
                metrics = f.read()
            messagebox.showinfo("Performance Metrics", metrics)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read metrics: {e}")

    def update_table(self):
        if not self.core:
            for lbl in self.value_labels:
                lbl.config(text="-")
            return
        state = self.core.state
        # Display key info for each stage
        stage_values = [
            f"PC: {state.IF.get('PC', '-')}",
            f"Instr: {format(state.ID.get('Instr', '-'), '032b') if state.ID.get('Instr', None) is not None else '-'}",
            f"Instr: {format(state.EX.get('instr', '-'), '032b') if state.EX.get('instr', None) is not None else '-'}",
            f'''ALU: {state.MEM.get('ALUresult', '-')}
Store: {state.MEM.get('Store_data', '-')}
Rd: {state.MEM.get('Wrt_reg_addr', '-')}
MemR: {state.MEM.get('rd_mem', '-')}
MemW: {state.MEM.get('wrt_mem', '-')}
WE: {state.MEM.get('wrt_enable', '-')}
M2R: {state.MEM.get('mem_to_reg', '-')}
NOP: {state.MEM.get('nop', '-')}
PC: {state.MEM.get('PC', '-')}''',
            f'''WData: {state.WB.get('Wrt_data', '-')}
Rd: {state.WB.get('Wrt_reg_addr', '-')}
WE: {state.WB.get('wrt_enable', '-')}
M2R: {state.WB.get('mem_to_reg', '-')}
ALU: {state.WB.get('ALUresult', '-')}
RData: {state.WB.get('read_data', '-')}
NOP: {state.WB.get('nop', '-')}''',
        ]
        for lbl, val in zip(self.value_labels, stage_values):
            lbl.config(text=val)

if __name__ == "__main__":
    root = tk.Tk()
    gui = PipelineGUI(root)
    root.mainloop() 