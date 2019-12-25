from opcode_computer import opcode_computer
import numpy as np
from collections import defaultdict

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

amplist_orig = copy(amplist)

complist = []
for ii in range(50):
    complist.append(opcode_computer(list(copy(list(amplist_orig)))+[0]*100000))
    complist[ii].input([ii])
    complist[ii].input([-1])

inpNotFound = True
NAT = None
yset = set()
while True:
    messagebuffer = defaultdict(list)
    nReading = 0
    for ii in range(50):
        address = complist[ii].run()
        if address == 'READING':
            nReading += 1
            continue
        xx = complist[ii].run()
        yy = complist[ii].run()
        print(ii,address,xx,yy)
        messagebuffer[address].append((xx,yy))
        if address == 255:
            NAT = (xx,yy)
    if nReading == 50:
        if NAT[1] in yset:
            print('FOUND IT', NAT[1])
            assert(1 == 0)
        else:
            yset.add(NAT[1])
        complist[0].input([NAT[0],NAT[1]])
        continue
    for ii in range(50):
        if ii not in messagebuffer:
            complist[ii].input([-1])
        else:
            for item in messagebuffer[ii]:
                complist[ii].input([item[0],item[1]])

