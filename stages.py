import G_MEM, G_UTL

# Control Unit ROM
# RegDst, ALUSrc, MemToReg, RegWrite, MemRead, MemWrite, Branch, AluOp
ctrl = {0b000000: (0b1, 0b0, 0b0, 0b1, 0b0, 0b0, 0b0, 0b10), # R-Type
        0b100011: (0b0, 0b1, 0b1, 0b1, 0b1, 0b0, 0b0, 0b00), # lw
        0b101011: (0b0, 0b1, 0b0, 0b0, 0b0, 0b1, 0b0, 0b00), # sw
        0b000100: (0b0, 0b0, 0b0, 0b0, 0b0, 0b0, 0b1, 0b01), # beq
        0b001000: (0b0, 0b1, 0b0, 0b1, 0b0, 0b0, 0b0, 0b00)} # addi

def EX_fwd():
    # Forwarding Unit
    if G_MEM.MEM_WB_CTRL['REG_WRITE'] == 1 and G_MEM.MEM_WB['RD'] != 0 and G_MEM.MEM_WB['RD'] == G_MEM.ID_EX['RS'] and (G_MEM.EX_MEM['RD'] != G_MEM.ID_EX['RS'] or G_MEM.EX_MEM_CTRL['REG_WRITE'] == 0):
        G_MEM.FWD['FWD_A'] = 1
    elif G_MEM.EX_MEM_CTRL['REG_WRITE'] == 1 and G_MEM.EX_MEM['RD'] != 0 and G_MEM.EX_MEM['RD'] == G_MEM.ID_EX['RS']:
        G_MEM.FWD['FWD_A'] = 2
    else:
        G_MEM.FWD['FWD_A'] = 0

    if G_MEM.MEM_WB_CTRL['REG_WRITE'] == 1 and G_MEM.MEM_WB['RD'] != 0 and G_MEM.MEM_WB['RD'] == G_MEM.ID_EX['RT'] and (G_MEM.EX_MEM['RD'] != G_MEM.ID_EX['RT'] or G_MEM.EX_MEM_CTRL['REG_WRITE'] == 0):
        G_MEM.FWD['FWD_B'] = 1
    elif G_MEM.EX_MEM_CTRL['REG_WRITE'] == 1 and G_MEM.EX_MEM['RD'] != 0 and G_MEM.EX_MEM['RD'] == G_MEM.ID_EX['RT']:
        G_MEM.FWD['FWD_B'] = 2
    else:
        G_MEM.FWD['FWD_B'] = 0

    # FwdA Multiplexer
    if G_MEM.FWD['FWD_A'] == 0 or not G_UTL.data_hzd:
        G_UTL.outFwdA = G_MEM.ID_EX['A']
    elif G_MEM.FWD['FWD_A'] == 1:
        if G_MEM.MEM_WB_CTRL['MEM_TO_REG'] == 1:
            G_UTL.outFwdA = G_MEM.MEM_WB['LMD']
        else:
            G_UTL.outFwdA = G_MEM.MEM_WB['ALU_OUT']
    elif G_MEM.FWD['FWD_A'] == 2:
        G_UTL.outFwdA = G_MEM.EX_MEM['ALU_OUT']

    # FwdB Multiplexer
    if G_MEM.FWD['FWD_B'] == 0 or not G_UTL.data_hzd:
        G_UTL.outFwdB = G_MEM.ID_EX['B']
    elif G_MEM.FWD['FWD_B'] == 1:
        # MemToReg Multiplexer
        if G_MEM.MEM_WB_CTRL['MEM_TO_REG'] == 1:
            G_UTL.outFwdB = G_MEM.MEM_WB['LMD']
        else:
            G_UTL.outFwdB = G_MEM.MEM_WB['ALU_OUT']
    elif G_MEM.FWD['FWD_B'] == 2:
        G_UTL.outFwdB = G_MEM.EX_MEM['ALU_OUT']

def ID_hzd():
    # Hazard Unit
    if_id_rs = (G_MEM.IF_ID['IR'] & 0x03E00000) >> 21 # IR[25..21]
    if_id_rt = (G_MEM.IF_ID['IR'] & 0x001F0000) >> 16 # IR[20..16]

    if G_MEM.ID_EX_CTRL['MEM_READ'] == 1 and (G_MEM.ID_EX['RT'] == if_id_rs or G_MEM.ID_EX['RT'] == if_id_rt) and G_UTL.data_hzd:
        G_MEM.FWD['PC_WRITE'] = 0
        G_MEM.FWD['IF_ID_WRITE'] = 0
        G_MEM.FWD['STALL'] = 1
    elif (G_MEM.ID_EX_CTRL['BRANCH'] == 1 or G_MEM.EX_MEM_CTRL['BRANCH'] == 1) and G_UTL.ctrl_hzd:
        G_MEM.FWD['IF_ID_WRITE'] = 0
        G_MEM.FWD['STALL'] = 1
    else:
        G_MEM.FWD['PC_WRITE'] = 1
        G_MEM.FWD['IF_ID_WRITE'] = 1
        G_MEM.FWD['STALL'] = 0

def IF():
    # Grab instruction from memory array
    try:
        curInst = G_MEM.INST[G_MEM.PC//4]
    except IndexError:
        curInst = 0

    # Set simulator flags
    G_UTL.ran['IF'] = (0, 0) if G_MEM.FWD['STALL'] == 1 else (G_MEM.PC//4, curInst)
    G_UTL.wasIdle['IF'] = (G_MEM.FWD['STALL'] == 1)

    if G_MEM.FWD['IF_ID_WRITE'] == 1 or not G_UTL.data_hzd:
        # Set IF/ID.NPC
        G_MEM.IF_ID['NPC'] = G_MEM.PC + 4

        # Set IF/ID.IR
        G_MEM.IF_ID['IR'] = curInst

    if G_MEM.FWD['PC_WRITE'] == 1 or not G_UTL.data_hzd:
        # Set own PC (PC Multiplexer)
        if G_MEM.EX_MEM['ZERO'] == 1 and G_MEM.EX_MEM_CTRL['BRANCH'] == 1:
            G_MEM.PC = G_MEM.EX_MEM['BR_TGT']
        elif G_MEM.FWD['STALL'] != 1:
            G_MEM.PC = G_MEM.PC + 4

def ID():
    # Set simulator flags
    G_UTL.ran['ID'] = (0, 0) if G_MEM.FWD['STALL'] == 1 else G_UTL.ran['IF']
    G_UTL.wasIdle['ID'] = (G_MEM.FWD['STALL'] == 1)

    if G_MEM.FWD['STALL'] == 1:
        # Stall the pipeline, adding a bubble
        G_MEM.ID_EX_CTRL['REG_DST'] = 0
        G_MEM.ID_EX_CTRL['ALU_SRC'] = 0
        G_MEM.ID_EX_CTRL['MEM_TO_REG'] = 0
        G_MEM.ID_EX_CTRL['REG_WRITE'] = 0
        G_MEM.ID_EX_CTRL['MEM_READ'] = 0
        G_MEM.ID_EX_CTRL['MEM_WRITE'] = 0
        G_MEM.ID_EX_CTRL['BRANCH'] = 0
        G_MEM.ID_EX_CTRL['ALU_OP'] = 0
    else:
        # Set Control of ID/EX (Control Unit)
        opcode = (G_MEM.IF_ID['IR'] & 0xFC000000) >> 26 # IR[31..26]
        G_MEM.ID_EX_CTRL['REG_DST'] = ctrl[opcode][0]
        G_MEM.ID_EX_CTRL['ALU_SRC'] = ctrl[opcode][1]
        G_MEM.ID_EX_CTRL['MEM_TO_REG'] = ctrl[opcode][2]
        G_MEM.ID_EX_CTRL['REG_WRITE'] = ctrl[opcode][3]
        G_MEM.ID_EX_CTRL['MEM_READ'] = ctrl[opcode][4]
        G_MEM.ID_EX_CTRL['MEM_WRITE'] = ctrl[opcode][5]
        G_MEM.ID_EX_CTRL['BRANCH'] = ctrl[opcode][6]
        G_MEM.ID_EX_CTRL['ALU_OP'] = ctrl[opcode][7]

    # Set ID/EX.NPC
    G_MEM.ID_EX['NPC'] = G_MEM.IF_ID['NPC']

    # Set ID/EX.A
    reg1 = (G_MEM.IF_ID['IR'] & 0x03E00000) >> 21 # IR[25..21]
    G_MEM.ID_EX['A'] = G_MEM.REGS[reg1]

    # Set ID/EX.B
    reg2 = (G_MEM.IF_ID['IR'] & 0x001F0000) >> 16 # IR[20..16]
    G_MEM.ID_EX['B'] = G_MEM.REGS[reg2]

    # Set ID/EX.RT
    G_MEM.ID_EX['RT'] = (G_MEM.IF_ID['IR'] & 0x001F0000) >> 16 # IR[20..16]

    # Set ID/EX.RD
    G_MEM.ID_EX['RD'] = (G_MEM.IF_ID['IR'] & 0x0000F800) >> 11 # IR[15..11]

    # Set ID/EX.Imm (Sign Extend)
    imm = (G_MEM.IF_ID['IR'] & 0x0000FFFF) >> 0 # IR[15..0]
    G_MEM.ID_EX['IMM'] = imm

    # Set ID/EX.RS
    G_MEM.ID_EX['RS'] = (G_MEM.IF_ID['IR'] & 0x03E00000) >> 21 # IR[25..21]

def EX():
    # Set simulator flags
    G_UTL.ran['EX'] = G_UTL.ran['ID']
    G_UTL.wasIdle['EX'] = False

    # Set Control of EX/MEM based on Control of ID/EX
    G_MEM.EX_MEM_CTRL['MEM_TO_REG'] = G_MEM.ID_EX_CTRL['MEM_TO_REG']
    G_MEM.EX_MEM_CTRL['REG_WRITE'] = G_MEM.ID_EX_CTRL['REG_WRITE']
    G_MEM.EX_MEM_CTRL['BRANCH'] = G_MEM.ID_EX_CTRL['BRANCH']
    G_MEM.EX_MEM_CTRL['MEM_READ'] = G_MEM.ID_EX_CTRL['MEM_READ']
    G_MEM.EX_MEM_CTRL['MEM_WRITE'] = G_MEM.ID_EX_CTRL['MEM_WRITE']

    # Set EX/MEM.BrTgt (Shift Left 2)
    G_MEM.EX_MEM['BR_TGT'] = G_MEM.ID_EX['NPC'] + (G_MEM.ID_EX['IMM'] << 2)

    # Set internal ALU source A
    aluA = G_UTL.outFwdA

    # Set internal ALU source B (B Multiplexer)
    if G_MEM.ID_EX_CTRL['ALU_SRC'] == 1:
        aluB = G_MEM.ID_EX['IMM']
    else:
        aluB = G_UTL.outFwdB

    # Set EX/MEM.Zero (ALU)
    if aluA - aluB == 0:
        G_MEM.EX_MEM['ZERO'] = 1
    else:
        G_MEM.EX_MEM['ZERO'] = 0

    # Set EX/MEM.AluOut (ALU + ALU Control)
    out = 0
    if G_MEM.ID_EX_CTRL['ALU_OP'] == 0: # Add (lw/sw/addi)
        out = aluA + aluB
    elif G_MEM.ID_EX_CTRL['ALU_OP'] == 1: # Sub (beq)
        out = aluA - aluB
    elif G_MEM.ID_EX_CTRL['ALU_OP'] == 2: # R-Type
        funct = G_MEM.ID_EX['IMM'] & 0x0000003F # IR[5..0]
        shamt = G_MEM.ID_EX['IMM'] & 0x000007C0 # IR[10..6]
        if funct == G_UTL.rTypeWords['add']:
            out = aluA + aluB
        elif funct == G_UTL.rTypeWords['sub']:
            out = aluA - aluB
        elif funct == G_UTL.rTypeWords['and']:
            out = aluA & aluB
        elif funct == G_UTL.rTypeWords['or']:
            out = aluA | aluB
        elif funct == G_UTL.rTypeWords['sll']:
            out = aluA << shamt
        elif funct == G_UTL.rTypeWords['srl']:
            out = aluA >> shamt
        elif funct == G_UTL.rTypeWords['xor']:
            out = aluA ^ aluB
        elif funct == G_UTL.rTypeWords['nor']:
            out = ~(aluA | aluB)
        elif funct == G_UTL.rTypeWords['mult']:
            out = aluA * aluB
        elif funct == G_UTL.rTypeWords['div']:
            out = aluA // aluB
    G_MEM.EX_MEM['ALU_OUT'] = out

    # Set EX/MEM.B
    G_MEM.EX_MEM['B'] = G_UTL.outFwdB

    # Set EX/MEM.RD (RegDst Multiplexer)
    if G_MEM.ID_EX_CTRL['REG_DST'] == 1:
        G_MEM.EX_MEM['RD'] = G_MEM.ID_EX['RD']
    else:
        G_MEM.EX_MEM['RD'] = G_MEM.ID_EX['RT']

def MEM():
    # Set simulator flags
    G_UTL.ran['MEM'] = G_UTL.ran['EX']
    G_UTL.wasIdle['MEM'] = G_MEM.EX_MEM_CTRL['MEM_READ'] != 1 and G_MEM.EX_MEM_CTRL['MEM_WRITE'] != 1

    # Set Control of MEM/WB based on Control of EX/MEM
    G_MEM.MEM_WB_CTRL['MEM_TO_REG'] = G_MEM.EX_MEM_CTRL['MEM_TO_REG']
    G_MEM.MEM_WB_CTRL['REG_WRITE'] = G_MEM.EX_MEM_CTRL['REG_WRITE']

    # Set MEM/WB.LMD (read from Data Memory)
    if G_MEM.EX_MEM_CTRL['MEM_READ'] == 1:
        # The simulation memory might not be big enough
        if G_MEM.EX_MEM['ALU_OUT']//4 < G_UTL.DATA_SIZE:
            G_MEM.MEM_WB['LMD'] = G_MEM.DATA[G_MEM.EX_MEM['ALU_OUT']//4]
        else:
            print('***WARNING***')
            print(f'\tMemory Read at position {G_MEM.EX_MEM["ALU_OUT"]} not executed:')
            print(f'\t\tMemory only has {G_UTL.DATA_SIZE*4} positions.')
            
            try:
                input('Press ENTER to continue execution or abort with CTRL-C. ')
            except KeyboardInterrupt:
                print('Execution aborted.')
                exit()
    
    # Write to Data Memory
    if G_MEM.EX_MEM_CTRL['MEM_WRITE'] == 1:
        # The simulation memory might not be big enough
        if G_MEM.EX_MEM['ALU_OUT']//4 < G_UTL.DATA_SIZE:
            G_MEM.DATA[G_MEM.EX_MEM['ALU_OUT']//4] = G_MEM.EX_MEM['B']
        else:
            print('***WARNING***')
            print(f'\tMemory Write at position {G_MEM.EX_MEM["ALU_OUT"]} not executed:')
            print(f'\t\tMemory only has {G_UTL.DATA_SIZE*4} positions.')
            
            try:
                input('Press ENTER to continue execution or abort with CTRL-C. ')
            except KeyboardInterrupt:
                print('Execution aborted.')
                exit()
    
    # Set MEM/WB.ALUOut
    G_MEM.MEM_WB['ALU_OUT'] = G_MEM.EX_MEM['ALU_OUT']

    # Set MEM/WB.RD
    G_MEM.MEM_WB['RD'] = G_MEM.EX_MEM['RD']

def WB():
    # Set simulator flags
    G_UTL.ran['WB'] = G_UTL.ran['MEM']
    G_UTL.wasIdle['WB'] = G_MEM.MEM_WB_CTRL['REG_WRITE'] != 1 or G_MEM.MEM_WB['RD'] == 0

    # Write to Registers
    if G_MEM.MEM_WB_CTRL['REG_WRITE'] == 1 and G_MEM.MEM_WB['RD'] != 0:
        # MemToReg Multiplexer
        if G_MEM.MEM_WB_CTRL['MEM_TO_REG'] == 1:
            G_MEM.REGS[G_MEM.MEM_WB['RD']] = G_MEM.MEM_WB['LMD']
        else:
            G_MEM.REGS[G_MEM.MEM_WB['RD']] = G_MEM.MEM_WB['ALU_OUT']