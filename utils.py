import instTranslator
import G_MEM, G_UTL

def readFile(filename):
    content = []
    with open(filename, 'r', encoding='UTF-8') as f:
        for l in f:
            s = l.strip()
            if s:
                content.append(s)

    return content

def printFwdAndHazard():
    print('               ╔═════════════[FORWARDING AND HAZARD UNITS]══════════════╗')
    if G_MEM.FWD['PC_WRITE'] == 1 and G_MEM.FWD['IF_ID_WRITE'] == 1 and G_MEM.FWD['FWD_A'] == 0 and G_MEM.FWD['FWD_B'] == 0:
        print('               ║ No action.                                             ║')
    else:
        if (G_MEM.FWD['PC_WRITE'] == 0 and G_MEM.FWD['IF_ID_WRITE'] == 0) or (G_MEM.ID_EX_CTRL['BRANCH'] == 1 or G_MEM.EX_MEM_CTRL['BRANCH'] == 1):
            print('               ║ Stalling (blocking write on PC and IF/ID)...           ║')

        if G_MEM.FWD['FWD_A'] != 0:
            print('               ║ FWD_A={} (MEM/WB.ALU_OUT -> A)...                       ║'.format(G_MEM.FWD['FWD_A']))

        if G_MEM.FWD['FWD_B'] != 0:
            print('               ║ FWD_B={} (MEM/WB.ALU_OUT -> Mux @ aluB and EX/MEM.B)... ║'.format(G_MEM.FWD['FWD_B']))
    print('               ╚════════════════════════════════════════════════════════╝')

def printPipelineRegs():
    print('╔════════════════════╦═══════════[PIPELINE REGISTERS]══════════╦════════════════════╗')
    print('║      [IF/ID]       ║      [ID/EX]       ║      [EX/MEM]      ║      [MEM/WB]      ║')
    print('║════════════════════╬════════════════════╬════════════════════╬════════════════════║')
    print('║                    ║     MEM_TO_REG=[{}] ║     MEM_TO_REG=[{}] ║     MEM_TO_REG=[{}] ║'.format(G_MEM.ID_EX_CTRL['MEM_TO_REG'], G_MEM.EX_MEM_CTRL['MEM_TO_REG'], G_MEM.MEM_WB_CTRL['MEM_TO_REG']))
    print('║                    ║      REG_WRITE=[{}] ║      REG_WRITE=[{}] ║      REG_WRITE=[{}] ║'.format(G_MEM.ID_EX_CTRL['REG_WRITE'], G_MEM.EX_MEM_CTRL['REG_WRITE'], G_MEM.MEM_WB_CTRL['REG_WRITE']))
    print('║                    ║         BRANCH=[{}] ║         BRANCH=[{}] ║                    ║'.format(G_MEM.ID_EX_CTRL['BRANCH'], G_MEM.EX_MEM_CTRL['BRANCH']))
    print('║                    ║       MEM_READ=[{}] ║       MEM_READ=[{}] ║                    ║'.format(G_MEM.ID_EX_CTRL['MEM_READ'], G_MEM.EX_MEM_CTRL['MEM_READ']))
    print('║                    ║      MEM_WRITE=[{}] ║      MEM_WRITE=[{}] ║                    ║'.format(G_MEM.ID_EX_CTRL['MEM_WRITE'], G_MEM.EX_MEM_CTRL['MEM_WRITE']))
    print('║                    ║        REG_DST=[{}] ║                    ║                    ║'.format(G_MEM.ID_EX_CTRL['REG_DST']))
    print('║                    ║        ALU_SRC=[{}] ║                    ║                    ║'.format(G_MEM.ID_EX_CTRL['ALU_SRC']))
    print('║                    ║        ALU_OP=[{:02b}] ║                    ║                    ║'.format(G_MEM.ID_EX_CTRL['ALU_OP']))
    print('╠════════════════════╬════════════════════╬════════════════════╬════════════════════╣')
    print('║     NPC=[{:08X}] ║     NPC=[{:08X}] ║  BR_TGT=[{:08X}] ║                    ║'.format(G_MEM.IF_ID['NPC'], G_MEM.ID_EX['NPC'], G_MEM.EX_MEM['BR_TGT']))
    print('║                    ║       A=[{:08X}] ║    ZERO=[{:08X}] ║     LMD=[{:08X}] ║'.format(G_MEM.ID_EX['A'], G_MEM.EX_MEM['ZERO'], G_MEM.MEM_WB['LMD']))
    print('║      IR=[{:08X}] ║       B=[{:08X}] ║ ALU_OUT=[{:08X}] ║                    ║'.format(G_MEM.IF_ID['IR'], G_MEM.ID_EX['B'], G_MEM.EX_MEM['ALU_OUT']))
    print('║                    ║      RT=[{:08X}] ║       B=[{:08X}] ║ ALU_OUT=[{:08X}] ║'.format(G_MEM.ID_EX['RT'], G_MEM.EX_MEM['B'], G_MEM.MEM_WB['ALU_OUT']))
    print('║                    ║      RD=[{:08X}] ║      RD=[{:08X}] ║      RD=[{:08X}] ║'.format(G_MEM.ID_EX['RD'], G_MEM.EX_MEM['RD'], G_MEM.MEM_WB['RD']))
    print('║                    ║     IMM=[{:08X}] ║                    ║                    ║'.format(G_MEM.ID_EX['IMM']))
    if G_UTL.data_hzd or G_UTL.ctrl_hzd:
        print('║                    ║      RS=[{:08X}] ║                    ║                    ║'.format(G_MEM.ID_EX['RS']))
    print('╚════════════════════╩════════════════════╩════════════════════╩════════════════════╝')

def printPC():
    print('                                   ╔════[PC]════╗')
    print('                                   ║ [{:08X}] ║'.format(G_MEM.PC))
    print('                                   ╚════════════╝')

def printInstMem():
    print('╔═════╦═════════════════════════════[PROGRAM]═══════════╦════════════════════════╗')

    for i in range(len(G_MEM.INST)):
        print('║ {:>3} ║ 0x{:08X} = 0b{:032b} ║ {:<22} ║'.format(i*4, G_MEM.INST[i], G_MEM.INST[i], instTranslator.decode(G_MEM.INST[i])))

    print('╚═════╩═════════════════════════════════════════════════╩════════════════════════╝')

def printRegMem():
    print('╔════════════════════╦═══════════════[REGISTERS]═══════════════╦════════════════════╗')
    print('║ $00[ 0]=[{:08X}] ║ $t0[ 8]=[{:08X}] ║ $s0[16]=[{:08X}] ║ $t8[24]=[{:08X}] ║'.format(G_MEM.REGS[0], G_MEM.REGS[8], G_MEM.REGS[16], G_MEM.REGS[24]))
    print('║ $at[ 1]=[{:08X}] ║ $t1[ 9]=[{:08X}] ║ $s1[17]=[{:08X}] ║ $t9[25]=[{:08X}] ║'.format(G_MEM.REGS[1], G_MEM.REGS[9], G_MEM.REGS[17], G_MEM.REGS[25]))
    print('║ $v0[ 2]=[{:08X}] ║ $t2[10]=[{:08X}] ║ $s2[18]=[{:08X}] ║ $k0[26]=[{:08X}] ║'.format(G_MEM.REGS[2], G_MEM.REGS[10], G_MEM.REGS[18], G_MEM.REGS[26]))
    print('║ $v1[ 3]=[{:08X}] ║ $t3[11]=[{:08X}] ║ $s3[19]=[{:08X}] ║ $k1[27]=[{:08X}] ║'.format(G_MEM.REGS[3], G_MEM.REGS[11], G_MEM.REGS[19], G_MEM.REGS[27]))
    print('║ $a0[ 4]=[{:08X}] ║ $t4[12]=[{:08X}] ║ $s4[20]=[{:08X}] ║ $gp[28]=[{:08X}] ║'.format(G_MEM.REGS[4], G_MEM.REGS[12], G_MEM.REGS[20], G_MEM.REGS[28]))
    print('║ $a1[ 5]=[{:08X}] ║ $t5[13]=[{:08X}] ║ $s5[21]=[{:08X}] ║ $sp[29]=[{:08X}] ║'.format(G_MEM.REGS[5], G_MEM.REGS[13], G_MEM.REGS[21], G_MEM.REGS[29]))
    print('║ $a2[ 6]=[{:08X}] ║ $t6[14]=[{:08X}] ║ $s6[22]=[{:08X}] ║ $fp[30]=[{:08X}] ║'.format(G_MEM.REGS[6], G_MEM.REGS[14], G_MEM.REGS[22], G_MEM.REGS[30]))
    print('║ $a3[ 7]=[{:08X}] ║ $t7[15]=[{:08X}] ║ $s7[23]=[{:08X}] ║ $ra[31]=[{:08X}] ║'.format(G_MEM.REGS[7], G_MEM.REGS[15], G_MEM.REGS[23], G_MEM.REGS[31]))
    print('╚════════════════════╩════════════════════╩════════════════════╩════════════════════╝')

def printDataMem():
    print('    ╔══════════════════╦═══════════════[MEMORY]══════════════╦══════════════════╗')

    memSize = len(G_MEM.DATA)
    for i in range(memSize//4):
        a, b, c, d = i*4, (memSize)+i*4, (memSize*2)+i*4, (memSize*3)+i*4
        print('    ║ [{:03}]=[{:08X}] ║ [{:03}]=[{:08X}] ║ [{:03}]=[{:08X}] ║ [{:03}]=[{:08X}] ║'.format(a, G_MEM.DATA[a//4], b, G_MEM.DATA[b//4], c, G_MEM.DATA[c//4], d, G_MEM.DATA[d//4]))        

    print('    ╚══════════════════╩══════════════════╩══════════════════╩══════════════════╝')

def printHistory(clkHistory):
    # Convert clkHistory to history board
    history = [[' ' for i in range(len(clkHistory))] for i in range(len(G_MEM.INST))]
    for i in range(len(clkHistory)):
        for exe in clkHistory[i]:
            if exe[2]: # Idle
                history[exe[1][0]][i] = ' '
                # history[exe[1][0]][i] = '(' + exe[0] + ')' # Show idle stages
            else:
                history[exe[1][0]][i] = exe[0]

    # Print header and column titles
    print('╔═════╦════════════════════════╦' + '═'*(6*len(clkHistory)) + '╗')
    print('║ Mem ║ ' + 'Clock #'.center(22) + ' ║', end='')
    for i in range(len(clkHistory)):
        print(str(i).center(5), end=' ')
    print('║')
    print('╠═════╬════════════════════════╬' + '═'*(6*len(clkHistory)) + '╣')

    # Print history board
    for i in range(len(history)):
        print('║ {:>3} ║ {:>22} ║'.format(i*4, instTranslator.decode(G_MEM.INST[i])), end='')
        for j in range(len(history[0])):
            print(history[i][j].center(5), end=' ')
        print('║')
    print('╚═════╩════════════════════════╩' + '═'*(6*len(clkHistory)) + '╝')