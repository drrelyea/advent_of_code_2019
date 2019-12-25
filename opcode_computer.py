# we might want to be able to assess the state of a VM
# the input codes might all be linked
# omg they might want a rewind capability... AAAAAAA

# with open('/Users/relyea/data/input.txt') as input_file:
#     inpstring = input_file.readlines()

# inpstring = inpstring[0].strip()
# amplist = inpstring.split(',')
# amplist = [int(a) for a in amplist]

# amplist_orig = copy(amplist)
# amplist_orig = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
# amplist_orig = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
# amplist_orig = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99] # outputs itself
# amplist_orig = [1102,34915192,34915192,7,4,7,99,0] puts out 1219070632396864

opcode_argtypes = {
    '01': ('VAL', 'VAL', 'ADDR'),
    '02': ('VAL', 'VAL', 'ADDR'),
    '03': ('ADDR',),
    '04': ('VAL',),
    '05': ('VAL', 'VAL'),
    '06': ('VAL', 'VAL'),
    '07': ('VAL', 'VAL', 'ADDR'),
    '08': ('VAL', 'VAL', 'ADDR'),
    '09': ('VAL',),
    '99': ()
}

# class opcode_input(object):
#     def __init__(self, input = None):
#         if input is not None:
#             self.input = [input]
#         else:
#             self.input = []
#     def update(input):
#         self.input = [input]

class opcode_computer(object):
    def __init__(self, input_code, thephase=None):
        self.current_index = 0
        self.input_code = input_code # this might share state between machines
        self.input_values = []
        if thephase is not None:
            self.input_values.append(thephase) # this may share state betwen machines
        self.input_index = 0
        self.output_values = []
        self.output_index = -1
        self.relative_base = 0
        self.unchanged_input = True

        self.phase_received = False        
        self.action_list = []
        # selt.state = 'NONE'

    def input(self, inputlist: list):
        self.input_values += inputlist
    
    def input_no_changes(self, inputlist: list):
        if not self.unchanged_input:
            print(inputlist)
            self.input_values += inputlist
            self.unchanged_input = True
        else:
            self.input_values[-1] = inputlist[0]
    
    def parseArguments(self, opcode, action_number):
        output_arguments = []
        for i_argument, argument in enumerate( opcode_argtypes[action_number]):
            if (
                len(opcode) < 2 + i_argument + 1 or
                opcode[-2 - i_argument -1 ] == '0'
            ):
                if argument == 'VAL':
                    the_argument = self.input_code[self.input_code[self.current_index + i_argument + 1]]
                elif argument == 'ADDR':
                    the_argument = self.input_code[self.current_index + i_argument + 1]
            elif opcode[-2 - i_argument - 1] == '1':
                if argument == 'VAL':
                    the_argument = self.input_code[self.current_index + i_argument + 1]
                elif argument == 'ADDR':
                    print('FAIL FAIL FAIL')
                    assert(1 == 0)
            elif opcode[-2 - i_argument - 1] == '2':
                if argument == 'VAL':
                    the_argument = self.input_code[self.input_code[self.current_index + i_argument + 1] + self.relative_base]
                elif argument == 'ADDR':
                    the_argument = self.input_code[self.current_index + i_argument + 1] + self.relative_base
            output_arguments.append(the_argument)
        return output_arguments
    
    def run(self):
        input_inst = 0
        while self.current_index < len(self.input_code):
            opcode = str(self.input_code[self.current_index])
            if len(opcode) == 1:
                opcode = '0'+opcode
            action_number = opcode[-2:]
            if action_number == '99':
                self.action_list.append(('END'))
                # print('DONE')
                return 'DONE'
            else:
                argument_list = self.parseArguments(opcode, action_number)
                # print('TEST: ', self.current_index, opcode, argument_list, self.input_values)
                self.reserve_current_index = self.current_index
                self.current_index = self.current_index + len(opcode_argtypes[action_number]) + 1
                if action_number == '03':
                    if self.input_index >= len(self.input_values):
                        self.current_index = self.reserve_current_index
                        return 'READING'
                    else:
                        self.input_code[argument_list[0]] = self.input_values[self.input_index]
                        # self.action_list.append(('INPUT', argument_list[0], self.input_index, self.input_code[argument_list[0]]))
                        self.input_index += 1
                        self.unchanged_input = False
                        # print('READ')
                elif action_number == '04':
                    self.output_index += 1
                    self.output_values.append(argument_list[0])
                    # self.action_list.append(('OUTPUT', self.output_index, argument_list[0]))
                    return self.output_values[self.output_index]
                    # print('OUTPUT: '+str(argument_list[0]))
                elif action_number == '01':
                    self.input_code[argument_list[2]] = argument_list[0] + argument_list[1]
                    # self.action_list.append(('ICWRITE_SUM', argument_list[2], self.input_code[argument_list[2]]))
                elif action_number == '02':
                    self.input_code[argument_list[2]] = argument_list[0] * argument_list[1]
                    # self.action_list.append(('ICWRITE_PRODUCT', argument_list[2], self.input_code[argument_list[2]]))
                elif action_number == '07':
                    self.input_code[argument_list[2]] = int(argument_list[0] < argument_list[1])
                    # self.action_list.append(('ICWRITE_COMPARISON_GT', argument_list[2], self.input_code[argument_list[2]]))
                elif action_number == '08':
                    self.input_code[argument_list[2]] = int(argument_list[0] == argument_list[1])
                    # self.action_list.append(('ICWRITE_COMPARISON_EQ', argument_list[2], self.input_code[argument_list[2]]))
                elif action_number == '05':
                    if argument_list[0] != 0:
                        # self.action_list.append(('INDEX_CHANGE_NEZERO', self.current_index, argument_list[1]))
                        self.current_index = argument_list[1]
                elif action_number == '06':
                    if argument_list[0] == 0:
                        # self.action_list.append(('INDEX_CHANGE_EQZERO', self.current_index, argument_list[1]))
                        self.current_index = argument_list[1]
                elif action_number == '09':
                    # self.action_list.append(('RELATIVE_BASE_CHANGE', self.relative_base, argument_list[0]))
                    self.relative_base += argument_list[0]

                else:
                    print("FAIL FAIL FAIL ACK")
                    print(opcode)
                    return -999
            # print('RESULT: ', ','.join([str(a) for a in self.input_code]))


# thegrid = np.zeros((510,510),dtype=int)
# thepos = (250,250)
# opreturn = 0
# facing = (0,1)
# facingdict = {
#     (0,1,0): (-1,0),
#     (0,1,1): (1,0),
#     (0,-1,0): (1,0),
#     (0,-1,1): (-1,0),
#     (1,0,0): (0,1),
#     (1,0,1): (0,-1),
#     (-1,0,0): (0,-1),
#     (-1,0,1): (0,1)
# }
# opcc = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
# position_set = set()
# numvisited = 0
# while type(opreturn) == int:
#     opcc.input([thegrid[thepos]])
#     color = opcc.run()
#     if type(color) != np.int64:
#         break
#     direction = opcc.run()
#     if thepos in position_set:
#         print('DUPE')
#     else:
#         numvisited += 1
#     print(numvisited, thepos, thegrid[thepos], color, direction, facing)
#     position_set.add(thepos)
#     thegrid[thepos] = color
#     facingkey = facing + (direction,)
#     facing = facingdict[facingkey]
#     thepos = (thepos[0] + facing[0], thepos[1] + facing[1])
