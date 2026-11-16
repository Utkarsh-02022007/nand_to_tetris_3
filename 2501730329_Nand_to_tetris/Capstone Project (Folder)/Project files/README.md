# Capstone: Make the Computer Draw a Box

**Student:** Utkarsh Yadav  
**Roll number:** 2501730329  
**K:** 29  
**Course:** Nand to Tetris – I (ETCCNT301)

## Personal calculations
- K = last two digits of roll number = 29
- K mod 3 = 2: assembler warns when a label is defined more than once.
- K mod 4 = 1: width = 16 × (1 + 1) = 32 pixels.
- Height = 20 rows; first row = 29.

## Files
- `assembler.py`: two-pass Hack assembler, predefined symbols, variables from RAM[16], duplicate-label warning.
- `Box.asm`: polls the keyboard and draws/clears the assigned rectangle.
- `Box.hack`: generated machine code for `Box.asm`.
- `hdl/CPU.hdl`, `hdl/Memory.hdl`, `hdl/Computer.hdl`: computer integration chips.
- `report.pdf`: short report.

## Generate the machine code
Run from this folder:
```bash
python3 assembler.py Box.asm
```

## Verification still required
Open the HDL files in the official Hardware Simulator and run the course test scripts. Open `Box.hack` in the CPU Emulator, load the keyboard test and capture your own screenshots. Put genuine screenshots in `screenshots/`. Do not submit blank placeholders as test evidence.
