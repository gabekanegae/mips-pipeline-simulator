ran = {"IF": (0, 0), "ID": (0, 0), "EX": (0, 0), "MEM": (0, 0), "WB": (0, 0)}
wasIdle = {"IF": False, "ID": False, "EX": False, "MEM": False, "WB": False}

rTypeWords = { "add": 0b100000, "sub": 0b100010, "and": 0b100100,  "or": 0b100101,
               "sll": 0b000000, "srl": 0b000010, "xor": 0b100110, "nor": 0b100111,
              "mult": 0b011000, "div": 0b011001}

rTypeBins = {v: k for k, v in rTypeWords.items()}

regNames = ["$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
              "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
              "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
              "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"]

REGS_SIZE = 32
DATA_SIZE = 16

EINST = -1
EARG = -2
EFLOW = -3
ERROR = [EINST, EARG, EFLOW]

fwd = True
outFwdA = 0
outFwdB = 0
stall = False