###
# File to store simulation registers, control signals and memory
###

import G_UTL

# Program Counter
PC = 0

# Instruction Memory
INST = []

# Registers
REGS = [0 for i in range(32)]

# Data Memory
DATA = [0 for i in range(G_UTL.DATA_SIZE)]

# Pipeline Registers
IF_ID = {'NPC': 0, 'IR': 0}
ID_EX = {'NPC': 0, 'A': 0, 'B': 0, 'RT': 0, 'RD': 0, 'IMM': 0, 'RS': 0}
EX_MEM = {'BR_TGT': 0, 'ZERO': 0, 'ALU_OUT': 0, 'B': 0, 'RD': 0}
MEM_WB = {'LMD': 0, 'ALU_OUT': 0, 'RD': 0}

# Control Signals
ID_EX_CTRL = {'REG_DST': 0, 'ALU_SRC': 0, 'MEM_TO_REG': 0, 'REG_WRITE': 0,
              'MEM_READ': 0, 'MEM_WRITE': 0, 'BRANCH': 0, 'ALU_OP': 0}
EX_MEM_CTRL = {'MEM_READ': 0, 'MEM_WRITE': 0, 'BRANCH': 0, 'MEM_TO_REG': 0, 'REG_WRITE': 0}
MEM_WB_CTRL = {'MEM_TO_REG': 0, 'REG_WRITE': 0}

# Forwarding Unit Signals
FWD = {'PC_WRITE': 1, 'IF_ID_WRITE': 1, 'FWD_A': 0, 'FWD_B': 0, 'STALL': 0}