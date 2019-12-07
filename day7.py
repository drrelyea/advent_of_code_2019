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
