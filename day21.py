from opcode_computer import opcode_computer
import numpy as np

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

amplist_orig = copy(amplist)

# current algo is simple
# # if there is land 4 spaces away, jump
# # if there is not land 4 spaces away, do not jump
# #   this means we can set T to not land, and then we can and 

# # if you see one, jump when it is 3 or 2 ahead if it is the only one
# # if you see three together, jump
#       j   j   j       
# #########.##.##.#.###
#       j   j   
# #########.#..########
#       j   j   j   j
# #########.#.#.##..###
#       j   j   j    
# ########.##.#.###
#       j   j   j   
# #######.#.#...#.###

# j   j   j   j    
# ###.##.##.#.###
# j   j   j    
# ##.##.#.###
# j   j   j
# ###.#..########
# j   j   j   j
# ###.#.#.##..###

# BEG
# ACEFGI but not BDFGH

# not CEGHI
# CFI
# not CFH
# CEF
# CEG

# CandNOTH

# B
# CFnotH or CJ

# (FnotH or J)andC

# NOT H T
# NOT T T
# NOT C J
# AND T J
# NOT B T
# OR T J






themap = []
# themap.append('OR D J\n')
# themap.append('NOT D T\n')

themap.append('NOT H T\n')
themap.append('NOT T T\n')
themap.append('NOT C J\n')
themap.append('AND T J\n')
themap.append('NOT B T\n')
themap.append('OR T J\n')
# always jump if pit right in front of you
themap.append('NOT A T\n')
themap.append('OR T J\n')
# do not jump if D is a pit
themap.append('NOT D T\n')
themap.append('NOT T T\n')
themap.append('AND T J\n')
themap.append('RUN\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('\n')
# themap.append('A,B,B,A,B,C,A,C,B,C\n')
# themap.append('L,4,L,6,L,8,L,6,6\n')
# themap.append('L,8,R,6,6,L,6,6\n')
# themap.append('R,6,6,L,6,L,6,L,8\n')

op = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
for line in themap:
    asciisequence = [ord(cc) for cc in line]
    print(asciisequence)
    op.input(asciisequence)

outputseq = []
newseq = []
for aa in op.run():
    if aa != 10:
        newseq.append(aa)
    elif aa == 10:
        outputseq.append(newseq)
        newseq = []

for line in outputseq:
    print(''.join(chr(aa) for aa in line))
