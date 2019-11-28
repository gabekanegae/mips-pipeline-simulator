# Load some data into memory
addi $t0, $zero, 15     # $t0 = 0xF
sw $t0, 0($zero)        # Copy $t0 to memory[0]
addi $t1, $zero, 240    # $t1 = 0xFF
sw $t1, 4($zero)        # Copy $t1 to memory[4]

# Do some calculations
# memory[8] = 0xFF * (0xF + 0xFF)

add $t3, $t0, $t1       # $t3 = $t0 + $t1
lw $t4, 4($zero)        # Copy memory[4] to $t4
mult $t5, $t4, $t3      # $t5 = $t4 * $t3
sw $t5, 8($zero)        # Copy $t5 to memory[8]

# Verify that the results are correct
# memory[8] = 240*(240+15) = 61200 = 0xEF10

lw $s0, 8($zero)  
addi, $s1, $zero, 61200
addi $s7, $zero, 1
beq $s0, $s1, 1
addi $s7, $s7, 1

# If correct, $s7 == 1.
# If not correct, $s7 == 2.