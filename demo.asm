lw $s0,0($t0)
lw $s1,4($t0)
beq $s0, $s1, 12
add $s3, $s4, $s5
not available instruction
j 24
sub $s3,$s4,$s5
sw $s3,8($t0)
addi $v0, $a0, 2