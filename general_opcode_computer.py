# we might want to be able to assess the state of a VM
# the input codes might all be linked
# omg they might want a rewind capability... AAAAAAA

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

amplist_orig = copy(amplist)
# amplist_orig = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
# amplist_orig = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

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
n_arguments_per_opcode = {
    '1': 2,
    '2': 2,
    '3': 0,
    '4': 1,
    '5': 2,
    '6': 2,
    '7': 2,
    '8': 2,
    '9': 0
}

class get_opcode_output(object):
    def __init__(self, input_code, thephase):
        self.current_index = 0
        self.input_code = input_code # this might share state between machines
        self.thephase = thephase
        self.input_values = [thephase] # this may share state betwen machines
        self.input_index = 0
        self.output_values = []
        self.output_index = -1

        self.phase_received = False        
        self.action_list = [] # this will contains state objects
        # a state object will either be a tuple of postion, old value, new value for writes
        # or it will be the index in the output list (and maybe the value for output, if we pop)
        # or it will be the index in the input list (and maybe the value of the input, if we pop)

    def parseArguments(self, opcode, action_number):
        output_arguments = []
        for i_argument in range(1, n_arguments_per_opcode[action_number]+1):
            if (
                len(opcode) < 2 + i_argument or
                opcode[-2 - i_argument] == '0'
            ):
                the_index = self.input_code[self.current_index + i_argument]
            else:
                the_index = self.current_index + i_argument
            the_argument = self.input_code[the_index]
            output_arguments.append(the_argument)
        return output_arguments
    
    def __call__(self, inputlist: list):
        self.input_values += inputlist
        input_inst = 0
        while self.current_index < len(self.input_code):
            opcode = str(self.input_code[self.current_index])
            action_number = opcode[-1]
            if action_number == '9':
                self.action_list.append(('END'))
                # print('DONE')
                return (100,100)
            else:
                argument_list = self.parseArguments(opcode, action_number)
                modifyIndex = self.input_code[self.current_index + to_modify_index_offset[action_number]]
                self.current_index = self.current_index + next_instruction_index_offset[action_number]
                # print('TEST: ', self.current_index, opcode, argument_list[0], argument_list[1], modifyIndex)
                if action_number == '3':
                    self.input_code[modifyIndex] = self.input_values[self.input_index]
                    self.action_list.append(('INPUT', modifyIndex, self.input_index, self.input_code[modifyIndex]))
                    self.input_index += 1
                elif action_number == '4':
                    self.output_index += 1
                    self.output_values.append(argument_list[0])
                    self.action_list.append(('OUTPUT', self.output_index, argument_list[0]))
                    return self.output_values[self.output_index]
                    # print('OUTPUT: '+str(argument_list[0]))
                elif action_number == '1':
                    self.input_code[modifyIndex] = argument_list[0] + argument_list[1]
                    self.action_list.append(('ICWRITE_SUM', modifyIndex, self.input_code[modifyIndex]))
                elif action_number == '2':
                    self.input_code[modifyIndex] = argument_list[0] * argument_list[1]
                    self.action_list.append(('ICWRITE_PRODUCT', modifyIndex, self.input_code[modifyIndex]))
                elif action_number == '7':
                    self.input_code[modifyIndex] = int(argument_list[0] < argument_list[1])
                    self.action_list.append(('ICWRITE_COMPARISON_GT', modifyIndex, self.input_code[modifyIndex]))
                elif action_number == '8':
                    self.input_code[modifyIndex] = int(argument_list[0] == argument_list[1])
                    self.action_list.append(('ICWRITE_COMPARISON_EQ', modifyIndex, self.input_code[modifyIndex]))
                elif action_number == '5':
                    if argument_list[0] != 0:
                        self.action_list.append(('INDEX_CHANGE_NEZERO', self.current_index, argument_list[1]))
                        self.current_index = argument_list[1]
                elif action_number == '6':
                    if argument_list[0] == 0:
                        self.action_list.append(('INDEX_CHANGE_EQZERO', self.current_index, argument_list[1]))
                        self.current_index = argument_list[1]

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
