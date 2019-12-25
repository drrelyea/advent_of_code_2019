# import pandas as pd
import numpy as np


"""
lessons about my code:
your recursion sucks - work on this
you turned L12 into L6,L6 - why? it's because you linked the L and the 12
NO HARDCODED CONSTANTS as they will change and you'll have a bug
get your indices straight when you have a list of lists! STICK TO A CONVENTION
upgrade your code to handle basic situations
    what happens when you don't have an input
    what happens when the input should overwrite instead of queue (or vv)
get ALL the requirements - you lost a lot of time missing specific cases that were mentioned
pay attention to signs - you lost an hour forgetting about them
pay attention to order - your brain sometimes assumes order AB and then order BA
    this is easiest if you create a data structure to handle it

BAD THINGS FROM AOC:
a lot of the solutions assume a limiting case trick
it does not teach you to code APIs
it does not reward you for abstraction layers
it teaches you to assume the problem is simple and solve it that way (like mazes that are acyclic)
"""












with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
v_size = 6
h_size = 25

im = np.array([int(char) for char in inpstring])
im = im.reshape((int(len(inpstring)/v_size/h_size),v_size,h_size))
layer = np.argmin(np.sum(im == 0,axis=(1,2)))
thesum = sum(im[layer,:,:] == 1) * sum(im[layer,:,:]==2)

newimage = np.zeros((v_size,h_size))
for ii in range(h_size):
    for jj in range(v_size):
        newimage[jj, ii] = im[im[:,jj, ii] != 2,jj, ii][0]








with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

amplist_orig = copy(amplist)
# amplist_orig = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
# amplist_orig = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

def getFirstArg(opcode, current_index, input_code):
    if opcode[-1] == '3':
        return -1
    elif len(opcode) < 3 or opcode[-3] == '0':
        return input_code[input_code[current_index+1]]
    else:
        return input_code[current_index+1]

def getSecondArg(opcode, current_index, input_code):
    if opcode[-1] == '3' or opcode[-1] == '4':
        return -1
    elif len(opcode) < 4 or opcode[-4] == '0':
        return input_code[input_code[current_index+2]]
    else:
        return input_code[current_index+2]

next_instruction_index_offset = {
    '1': 4,
    '2': 4,
    '3': 2,
    '4': 2,
    '5': 3,
    '6': 3,
    '7': 4,
    '8': 4,
    '9': 2
}
to_modify_index_offset = {
    '1': 3,
    '2': 3,
    '3': 1,
    '4': 0,
    '5': 0,
    '6': 0,
    '7': 3,
    '8': 3,
    '9': 0
}

class get_opcode_output(object):
    def __init__(self, input_code, thephase):
        self.current_index = 0
        self.input_code = input_code
        self.thephase = thephase
        self.phase_received = False
        self.the_output = 0

    def __call__(self, inputlist):
        input_inst = 0
        while self.current_index < len(self.input_code):
            opcode = str(self.input_code[self.current_index])
            action_number = opcode[-1]
            if action_number == '9':
                # print('DONE')
                return (self.the_output,100)
            else:
                firstArg = getFirstArg(opcode, self.current_index, self.input_code)
                secondArg = getSecondArg(opcode, self.current_index, self.input_code)
                modifyIndex = self.input_code[self.current_index + to_modify_index_offset[action_number]]
                self.current_index = self.current_index + next_instruction_index_offset[action_number]
                # print('TEST: ', self.current_index, opcode, firstArg, secondArg, modifyIndex)
                if action_number == '3':
                    if not self.phase_received:
                        self.input_code[modifyIndex] = self.thephase
                        self.phase_received = True
                    else:
                        self.input_code[modifyIndex] = inputlist[input_inst]
                        input_inst += 1
                elif action_number == '4':
                    self.the_output = firstArg
                    return self.the_output
                    # print('OUTPUT: '+str(firstArg))
                elif action_number == '1':
                    self.input_code[modifyIndex] = firstArg + secondArg
                elif action_number == '2':
                    self.input_code[modifyIndex] = firstArg * secondArg
                elif action_number == '7':
                    self.input_code[modifyIndex] = int(firstArg < secondArg)
                elif action_number == '8':
                    self.input_code[modifyIndex] = int(firstArg == secondArg)
                elif action_number == '5':
                    if firstArg != 0:
                        self.current_index = secondArg
                elif action_number == '6':
                    if firstArg == 0:
                        self.current_index = secondArg

                else:
                    print("FAIL FAIL FAIL ACK")
                    print(opcode)
                    return -999
            # print('RESULT: ', ','.join([str(a) for a in self.input_code]))



themax = 0
from itertools import permutations 
l = list(permutations(range(5,10)))
for thephase in l:
    amplifiers = [get_opcode_output(copy(list(amplist_orig)),thephase[ii]) for ii in range(5)]
    input_inst = 0
    ampnum = 0
    while type(input_inst) != tuple:
        old_input_inst = copy(input_inst)
        input_inst = amplifiers[ampnum]([input_inst])
        print(ampnum, input_inst)
        ampnum = (ampnum + 1) % 5
    print(old_input_inst, thephase)
    if old_input_inst > themax:
        best_seq = copy(thephase)
        themax = old_input_inst












with open('/Users/relyea/data/input.txt') as input_file:
    orbit_relations = input_file.readlines()

orbit_relations = [aa.strip() for aa in orbit_relations]

orbits = {}
for pair in orbit_relations:
    orbited, orbiting = pair.split(')')
    if orbited not in orbits:
        orbits[orbited] = [orbiting]
    else:
        orbits[orbited].append(orbiting)

ndirect = 0
nindirect = 0

nindirect_dict = {}

def count_indirect(planet):
    if planet in nindirect_dict:
        return nindirect_dict[planet]
    else:        
        nindirect_dict[planet] = 0
        orbiters = orbits[planet]
        for orbiter in orbiters:
            if orbiter in orbits:
                nindirect_dict[planet] += len(orbits[orbiter])
                nindirect_dict[planet] += count_indirect(orbiter)
    return nindirect_dict[planet]

for planet in orbits:
    for orbiter in orbits[planet]:
        ndirect += 1
    nindirect += count_indirect(planet)

orbitings = {}
for pair in orbit_relations:
    orbited, orbiting = pair.split(')')
    if orbiting not in orbitings:
        orbitings[orbiting] = orbited


[rr for rr in orbit_relations if 'YOU' in rr] # MV2
[rr for rr in orbit_relations if 'SAN' in rr] # R5H

#find common node

current = 'YOU'
ii = 0
tree_counts = []
tree_nocounts = []
while current in orbitings:
    tree_counts.append((current, ii))
    tree_nocounts.append(current)
    ii += 1
    current = orbitings[current]

current = 'SAN'
ii = 0
santree_counts = []
santree_nocounts = []
while current in orbitings:
    santree_counts.append((current, ii))
    santree_nocounts.append(current)
    ii += 1
    current = orbitings[current]

for element in tree_nocounts:
    if element in santree_nocounts:
        print(element, tree_nocounts.index(element), santree_nocounts.index(element))
        break














# 7161591
with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
input_code = inpstring.split(',')
input_code = [int(a) for a in input_code]

# input_code = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
# 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
# 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

the_input = 6

def getFirstArg(opcode, current_index, input_code):
    if opcode[-1] == '3':
        return -1
    elif len(opcode) < 3 or opcode[-3] == '0':
        return input_code[input_code[current_index+1]]
    else:
        return input_code[current_index+1]

def getSecondArg(opcode, current_index, input_code):
    if opcode[-1] == '3' or opcode[-1] == '4':
        return -1
    elif len(opcode) < 4 or opcode[-4] == '0':
        return input_code[input_code[current_index+2]]
    else:
        return input_code[current_index+2]

next_instruction_index_offset = {
    '1': 4,
    '2': 4,
    '3': 2,
    '4': 2,
    '5': 3,
    '6': 3,
    '7': 4,
    '8': 4,
    '9': 2
}
to_modify_index_offset = {
    '1': 3,
    '2': 3,
    '3': 1,
    '4': 0,
    '5': 0,
    '6': 0,
    '7': 3,
    '8': 3,
    '9': 0
}
current_index = 0
new_current_index = 0
while current_index < len(input_code):
    opcode = str(input_code[current_index])
    action_number = opcode[-1]
    if action_number == '9':
        print('DONE')
        break
    else:
        new_current_index = current_index + next_instruction_index_offset[action_number]
        firstArg = getFirstArg(opcode, current_index, input_code)
        secondArg = getSecondArg(opcode, current_index, input_code)
        modifyIndex = input_code[current_index + to_modify_index_offset[action_number]]
        # print('TEST: ', current_index, opcode, firstArg, secondArg, modifyIndex)
        if action_number == '3':
            input_code[modifyIndex] = the_input 
        elif action_number == '4':
            print('OUTPUT: '+str(firstArg))
        elif action_number == '1':
            input_code[modifyIndex] = firstArg + secondArg
        elif action_number == '2':
            input_code[modifyIndex] = firstArg * secondArg
        elif action_number == '7':
            input_code[modifyIndex] = int(firstArg < secondArg)
        elif action_number == '8':
            input_code[modifyIndex] = int(firstArg == secondArg)
        elif action_number == '5':
            if firstArg != 0:
                new_current_index = secondArg
        elif action_number == '6':
            if firstArg == 0:
                new_current_index = secondArg

        else:
            print("FAIL FAIL FAIL ACK")
            print(opcode)
            break
    # print('RESULT: ', ','.join([str(a) for a in input_code]))
    current_index = new_current_index






















goodcounter = 0
for ii in range(235741,706948):
    thestr = str(ii)
    if (
        int(thestr[0]) <= int(thestr[1]) and
        int(thestr[1]) <= int(thestr[2]) and
        int(thestr[2]) <= int(thestr[3]) and
        int(thestr[3]) <= int(thestr[4]) and
        int(thestr[4]) <= int(thestr[5])
    ):
        if (
            (thestr[0] == thestr[1] and thestr[1] != thestr[2]) or 
            (thestr[1] == thestr[2] and thestr[0] != thestr[1] and thestr[2] != thestr[3]) or 
            (thestr[2] == thestr[3] and thestr[1] != thestr[2] and thestr[3] != thestr[4]) or 
            (thestr[3] == thestr[4] and thestr[2] != thestr[3] and thestr[4] != thestr[5]) or 
            (thestr[4] == thestr[5] and thestr[3] != thestr[4])
         ):
            goodcounter += 1











with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring_one = inpstring[0].strip()
input_code_one = inpstring_one.split(',')
inpstring_two = inpstring[1].strip()
input_code_two = inpstring_two.split(',')

# input_code_one = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']
# input_code_two = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
current_spot = (0,0)
first_wire = [current_spot]
for code in input_code_one:
    distance = int(code[1:])
    if code[0] == 'L':
        for ii in range(distance):
            first_wire.append((current_spot[0]+ii+1,current_spot[1]))
        current_spot = (current_spot[0]+distance,current_spot[1])
    elif code[0] == 'R':
        for ii in range(distance):
            first_wire.append((current_spot[0]-ii-1,current_spot[1]))
        current_spot = (current_spot[0]-distance,current_spot[1])
    elif code[0] == 'D':
        for ii in range(distance):
            first_wire.append((current_spot[0],current_spot[1]-ii-1))
        current_spot = (current_spot[0],current_spot[1]-distance)
    elif code[0] == 'U':
        for ii in range(distance):
            first_wire.append((current_spot[0],current_spot[1]+ii+1))
        current_spot = (current_spot[0],current_spot[1]+distance)

current_spot = (0,0)
second_wire = [current_spot]
for code in input_code_two:
    distance = int(code[1:])
    if code[0] == 'L':
        for ii in range(distance):
            second_wire.append((current_spot[0]+ii+1,current_spot[1]))
        current_spot = (current_spot[0]+distance,current_spot[1])
    elif code[0] == 'R':
        for ii in range(distance):
            second_wire.append((current_spot[0]-ii-1,current_spot[1]))
        current_spot = (current_spot[0]-distance,current_spot[1])
    elif code[0] == 'D':
        for ii in range(distance):
            second_wire.append((current_spot[0],current_spot[1]-ii-1))
        current_spot = (current_spot[0],current_spot[1]-distance)
    elif code[0] == 'U':
        for ii in range(distance):
            second_wire.append((current_spot[0],current_spot[1]+ii+1))
        current_spot = (current_spot[0],current_spot[1]+distance)

crossings = set(first_wire).intersection(set(second_wire))
mindist = 100000000
for cc in list(crossings):
    newdist = first_wire.index(cc) + second_wire.index(cc)
    if newdist > 0 and newdist < mindist:
        newbest = cc
        mindist = newdist
cc = [abs(aa[0]) + abs(aa[1]) for aa in list(crossings)]



with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
input_code = inpstring.split(',')
input_code = [int(a) for a in input_code]
input_code[1] = 12
input_code[2] = 2

# input_code = [1,0,0,0,99]
# input_code = [2,3,0,3,99]
# input_code = [2,4,4,5,99,0]
# input_code = [1,1,1,4,99,5,6,0,99]

input_code_copy = copy(input_code)
for aa in range(100):
    for bb in range(100):
        # print(aa,bb)
        input_code = inpstring.split(',')
        input_code = [int(a) for a in input_code]
        input_code[1] = aa
        input_code[2] = bb
        for ii in range(np.int(np.floor(len(input_code)/4))):
            the_index = ii*4
            if input_code[the_index] == 99:
                break
            elif (
                input_code[the_index+1] >= len(input_code) or 
                input_code[the_index+2] >= len(input_code) or 
                input_code[the_index+3] >= len(input_code)
            ):
                print('ACK FAIL FAIL'+str(ii)+'   '+str(aa)+'   '+str(bb))
                break
            elif input_code[the_index] == 1:
                input_code[input_code[the_index+3]] = input_code[input_code[the_index+1]] + input_code[input_code[the_index+2]]
            elif input_code[the_index] == 2:
                input_code[input_code[the_index+3]] = input_code[input_code[the_index+1]] * input_code[input_code[the_index+2]]
            else:
                print('ACK FAIL FAIL'+str(ii)+'   '+str(aa)+'   '+str(bb))
                break
        if input_code[0] == 19690720:
            print(aa,bb)

def modify_code(input_code, the_index):


aa = pd.read_csv('/Users/relyea/data/input.txt',header=None)
np.sum(np.floor(aa[0]/3)-2)

def getFuel(fuel_inp):
    fuel_needed = np.floor(fuel_inp/3)-2
    if fuel_needed <= 0:
        return 0
    else:
        return fuel_needed + getFuel(fuel_needed)
