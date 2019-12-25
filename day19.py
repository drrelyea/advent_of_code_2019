from opcode_computer import opcode_computer
import numpy as np

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

bigamplist = amplist + [0]*1000

amplist_orig = copy(bigamplist)

N = 10000
thelist = []
thegrid = np.zeros((N,N))
square_not_found = True
ii = 4
jj = 0
prior_jj = 0
while square_not_found:
    jj = prior_jj
    beam_not_found = True
    while beam_not_found:
        op = opcode_computer(list(copy(list(amplist_orig))))
        op.input([ii,jj])
        beam = [aa for aa in op.run()][0]
        if beam != 1:
            jj += 1
        else:
            print(ii,jj,prior_jj)
            prior_jj = jj
            beam_not_found = False
            if ii >= 99:
                opposite_ii = ii - 99
                opposite_jj = jj + 99
                op = opcode_computer(list(copy(list(amplist_orig))))
                op.input([opposite_ii,opposite_jj])
                beam = [aa for aa in op.run()][0]
                if beam == 1:
                    print(opposite_ii, opposite_jj)
                    square_not_found = False
            ii += 1
