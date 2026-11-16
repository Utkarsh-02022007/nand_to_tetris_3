#!/usr/bin/env python3
"""
Minimal two-pass assembler for the Hack computer (Nand2Tetris).
Student: Utkarsh Yadav | Roll: 2501730329 | K = 29
K mod 3 = 2: warn when a label is defined more than once.
"""
import re
import sys
from pathlib import Path

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}
COMP = {
    "0":"0101010", "1":"0111111", "-1":"0111010",
    "D":"0001100", "A":"0110000", "!D":"0001101", "!A":"0110001",
    "-D":"0001111", "-A":"0110011", "D+1":"0011111", "A+1":"0110111",
    "D-1":"0001110", "A-1":"0110010", "D+A":"0000010", "D-A":"0010011",
    "A-D":"0000111", "D&A":"0000000", "D|A":"0010101",
    "M":"1110000", "!M":"1110001", "-M":"1110011", "M+1":"1110111",
    "M-1":"1110010", "D+M":"1000010", "D-M":"1010011",
    "M-D":"1000111", "D&M":"1000000", "D|M":"1010101"
}
PREDEFINED = {
    "SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4,
    **{f"R{i}":i for i in range(16)},
    "SCREEN":16384, "KBD":24576
}

def clean_lines(source):
    cleaned = []
    for original_no, raw in enumerate(source.splitlines(), 1):
        line = raw.split("//", 1)[0].strip()
        if line:
            cleaned.append((original_no, re.sub(r"\s+", "", line)))
    return cleaned

def assemble(source):
    lines = clean_lines(source)
    symbols = dict(PREDEFINED)
    labels_seen = set()
    rom = 0
    # Pass 1: labels
    for line_no, line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if not label or not re.fullmatch(r"[A-Za-z_.$:][\w.$:]*", label):
                raise ValueError(f"Line {line_no}: invalid label")
            if label in labels_seen:
                print(f"Warning: Line {line_no}: duplicate label '{label}'")
            else:
                symbols[label] = rom
                labels_seen.add(label)
        else:
            rom += 1

    # Pass 2: instructions and variables
    next_variable = 16
    machine = []
    for line_no, line in lines:
        if line.startswith("(") and line.endswith(")"):
            continue
        try:
            if line.startswith("@"):
                value = line[1:]
                if value.isdigit():
                    address = int(value)
                elif value in symbols:
                    address = symbols[value]
                else:
                    if not re.fullmatch(r"[A-Za-z_.$:][\w.$:]*", value):
                        raise ValueError("invalid symbol")
                    address = next_variable
                    symbols[value] = address
                    next_variable += 1
                if not 0 <= address <= 32767:
                    raise ValueError("A-instruction address out of range")
                machine.append(f"{address:016b}")
            else:
                if line.count("=") > 1 or line.count(";") > 1:
                    raise ValueError("malformed C-instruction")
                if ";" in line:
                    left, jump = line.split(";", 1)
                    if jump not in JUMP:
                        raise ValueError("invalid jump")
                else:
                    left, jump = line, ""
                if "=" in left:
                    dest, comp = left.split("=", 1)
                    if dest not in DEST:
                        raise ValueError("invalid destination")
                else:
                    dest, comp = "", left
                if comp not in COMP:
                    raise ValueError(f"invalid computation '{comp}'")
                machine.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
        except ValueError as exc:
            raise ValueError(f"Line {line_no}: {exc}") from None
    return machine, symbols

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 assembler.py input.asm")
        raise SystemExit(2)
    source_path = Path(sys.argv[1])
    try:
        machine, symbols = assemble(source_path.read_text(encoding="utf-8"))
        output_path = source_path.with_suffix(".hack")
        output_path.write_text("\n".join(machine) + "\n", encoding="utf-8")
        print(f"Assembled {len(machine)} instructions -> {output_path}")
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
