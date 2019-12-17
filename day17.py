from opcode_computer import opcode_computer
import numpy as np

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

amplist_orig = copy(amplist)

thelist = []
op = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
internallist = []
for output in op.run():
    if output != 10:
        internallist.append(output)
    else:
        thelist.append(internallist)
        internallist = []
thelist = thelist[:-1]
xsize = len(thelist)
ysize = len(thelist[0])
scaffold = np.array(thelist)
scaffold_sum  =0
for ii in range(1,scaffold.shape[0]-1):
    for jj in range(1, scaffold.shape[1]-1):
        if (
            scaffold[ii,jj] == 35 and
            scaffold[ii+1,jj] == 35 and
            scaffold[ii-1,jj] == 35 and
            scaffold[ii,jj+1] == 35 and
            scaffold[ii,jj-1] == 35
        ):
            print(ii,jj)
            scaffold_sum += ii*jj

asciimap = {
    35: '#',
    46: '.',
    94: '^'
}
# robot is at 18,32
easytosee = []
for ii in thelist:
    newline = []
    for jj in ii:
        newline.append(asciimap[jj])
    easytosee.append(''.join(newline))

asciimap = {
    'A': 65,
    'B': 66,
    'C': 67,
    'L': 76,
    'R': 82,
    ',': 44,
    'e': 10,
    '1': 49,
    '2': 50,
    '4': 52,
    '6': 54,
    '8': 56,
}



# A L 4 L 6 L 8 L 12 
# B L 8 R 12 L 12 
# B L 8 R 12 L 12 
# A L 4 L 6 L 8 L 12
# B L 8 R 12 L 12 
# C R 12 L 6 L 6 L 8
# A L 4 L 6 L 8 L 12 
# C R 12 L 6 L 6 L 8 
# B L 8 R 12 L 12 
# C R 12 L 6 L 6 L 8

themap = []
themap.append('A,B,B,A,B,C,A,C,B,Ce')
themap.append('L,4,L,6,L,8,L,6,6e')
themap.append('L,8,R,6,6,L,6,6e')
themap.append('R,6,6,L,6,L,6,L,8e')

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

amplist_orig = copy(amplist)
amplist_orig[0] = 2
op = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
for line in themap:
    asciisequence = [asciimap[cc] for cc in line]
    print(asciisequence)
    op.input(asciisequence)
op.input([110,10])

for aa in op.run()
    print(aa)
