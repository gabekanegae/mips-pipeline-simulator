import sys
import instTranslator
import stages
from utils import *

import G_MEM, G_UTL

def main():
    filename = "program.asm"

    # Read .asm
    program = loadProgram(filename)
    programLength = len(program)

    # Encode and load .asm into memory
    for i in range(programLength):
        if not program[i] or program[i][0] == "#":
            continue

        encoded = instTranslator.encode(program[i].split("#")[0])
        if encoded not in G_UTL.ERROR:
            G_MEM.INST.append(encoded)
        else:
            print("ERROR @ '{}':".format(filename))
            print("\tLine {}: '{}'".format(i+1, program[i]))
            if encoded == G_UTL.EINST:
                print("\t\tCouldn't parse the instruction")
            elif encoded == G_UTL.EARG:
                print("\t\tCouldn't parse one or more arguments")
            elif encoded == G_UTL.EFLOW:
                print("\t\tOne or more arguments are under/overflowing")
            return

    # Print the interpreted program
    printInstMem()
    print()

    # Don't print memory after each clock
    silent = ("-s" in sys.argv)

    # Run simulation
    clkHistory = []
    clk = 0
    while clk == 0 or (G_UTL.ran["IF"][1] != 0 or G_UTL.ran["ID"][1] != 0
                       or G_UTL.ran["EX"][1] != 0 or G_UTL.ran["MEM"][1] != 0):
        if silent:
            print("─"*20 + " CLK #{} ".format(clk) + "─"*20)
        else:
            print("─"*42 + " CLK #{} ".format(clk) + "─"*42)
            printPC()

        clkHistory.append([])

        # Run all stages "in parallel"
        stages.WB()
        stages.MEM()
        stages.EX()
        stages.ID()
        stages.IF()

        # Keep only the 32 LSB from memory
        for i in range(len(G_MEM.REGS)):
            G_MEM.REGS[i] &= 0xFFFFFFFF
        for i in range(len(G_MEM.DATA)):
            G_MEM.DATA[i] &= 0xFFFFFFFF

        # Report if stage was run
        for stage in ["IF", "ID", "EX", "MEM", "WB"]:
            if G_UTL.ran[stage][1] != 0:
                b = " (idle)" if G_UTL.wasIdle[stage] else ""
                clkHistory[clk].append((stage, G_UTL.ran[stage], G_UTL.wasIdle[stage]))
                print("> Stage {}: #{} = [{}]{}.".format(stage, G_UTL.ran[stage][0]*4,
                                                         instTranslator.decode(G_UTL.ran[stage][1]), b))

        # Print resulting memory
        if not silent:
            printTempRegs()
            printRegMem()
            printDataMem()
        clk += 1

    print()
    print("Empty pipeline, ending execution...")
    print("Program ran in {} clocks.".format(clk))
    print()

    printHistory(clkHistory)
    return

if __name__ == "__main__":
    # To print (pipe to file) pretty borders on Windows
    if sys.platform == "win32": 
        sys.stdout.reconfigure(encoding="UTF-8")

    main()