# > 	Increment the data pointer by one (to point to the next cell to the right).
# < 	Decrement the data pointer by one (to point to the next cell to the left).
# + 	Increment the byte at the data pointer by one.
# - 	Decrement the byte at the data pointer by one.
# . 	Output the byte at the data pointer.
# , 	Accept one byte of input, storing its value in the byte at the data pointer.
# [ 	If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
# ] 	If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.[a]

import sys
mem = [0]
malloc = 0
memloc = 0
ign = []
oPos = []
bNum = 0
readPos = 0
with open(sys.argv[1]) as f:
    s = f.read()    
    l = len(s)
    while readPos < l:
        if not ign or (ign and not ign[-1]) or s[readPos]=="]":
            match s[readPos]:
                case ">":
                    memloc += 1
                    if memloc > malloc:
                        malloc += 1
                        mem.append(0)
                case "<":
                    memloc = memloc-1 if memloc else 0
                case "+":
                    mem[memloc] += 1
                case "-":
                    mem[memloc] -= 1
                case ".":
                    print(chr(mem[memloc]), end="")
                case ",":
                    mem[memloc] = ord(input()[0])
                case "[":
                    oPos.append(readPos)
                    ign.append(not mem[memloc])
                case "]":
                    if mem[memloc]:
                        readPos = oPos[-1]
                    else:
                        ign.pop()
                        oPos.pop()
        readPos += 1
print("")