import G_UTL

PC = 0

INST = []
REGS = [0 for i in range(G_UTL.REGS_SIZE)]
DATA = [0 for i in range(G_UTL.DATA_SIZE)]
DATA[0] = 0xFF

IF_ID = {"NPC": 0, "IR": 0}
ID_EX = {"NPC": 0, "A": 0, "B": 0, "RT": 0, "RD": 0, "IMM": 0, "RS": 0}
EX_MEM = {"BR_TGT": 0, "ZERO": 0, "ALU_OUT": 0, "B": 0, "RD": 0}
MEM_WB = {"LMD": 0, "ALU_OUT": 0, "RD": 0}

ID_EX_CTRL = {"REG_DST": 0, "ALU_SRC": 0, "MEM_TO_REG": 0, "REG_WRITE": 0,
              "MEM_READ": 0, "MEM_WRITE": 0, "BRANCH": 0, "ALU_OP": 0}
EX_MEM_CTRL = {"MEM_READ": 0, "MEM_WRITE": 0, "BRANCH": 0, "MEM_TO_REG": 0, "REG_WRITE": 0}
MEM_WB_CTRL = {"MEM_TO_REG": 0, "REG_WRITE": 0}

FWD = {"PC_WRITE": 1, "IF_ID_WRITE": 1, "FWD_A": 0, "FWD_B": 0}