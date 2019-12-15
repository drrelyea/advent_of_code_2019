from opcode_computer import opcode_computer
import numpy as np

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

amplist_orig = copy(amplist)

ordered_directions_map = (
    (1,4,2,3),
    (4,2,3,1),
    (2,3,1,4),
    (3,1,4,2),
    (1,3,2,4),
    (3,2,4,1),
    (2,4,1,3),
    (4,1,3,2)
)

def update_position(direction, position):
    if direction == 1:
        newposition = (position[0], position[1]+1)
    elif direction == 2:
        newposition = (position[0], position[1]-1)
    elif direction == 3:
        newposition = (position[0]+1, position[1])
    elif direction == 4:
        newposition = (position[0]-1, position[1])
    return newposition

def wall_in_that_direction(layout, position, direction):
    if layout[update_position(direction, position)] == 1:
        return True
    else:
        return False

def find_next_direction(layout, index_of_directions_to_try, index_of_directions_to_try_offset, position, ordered_directions):
    notFound = True
    if index_of_directions_to_try[position] == -1:
        index_of_directions_to_try[position] = index_of_directions_to_try_offset[position]
    while notFound:
        nextDirection = ordered_directions[index_of_directions_to_try[position]]
        print('FINDING', position, nextDirection)
        index_of_directions_to_try[position] = ( index_of_directions_to_try[position] + 1 ) % 4
        if not wall_in_that_direction(layout, position, nextDirection):
            notFound = False
    return nextDirection

def update_attempted_directions(direction, position, index_of_directions_to_try_offset, ordered_directions):
    if index_of_directions_to_try_offset[position] == -1:
        index_of_directions_to_try_offset[position] = ( ordered_directions.index(direction) + 3 ) % 4

def put_wall_in_direction(direction, position, layout):
    layout[update_position(direction, position)] = 1


states = set()

layouts = np.zeros((8,51,51))

for ilayout in range(len(ordered_directions_map)):
    layout = np.zeros((51,51)) - 1
    index_of_directions_to_try = np.zeros((51,51),dtype=int) - 1
    index_of_directions_to_try_offset = np.zeros((51,51),dtype=int) - 1
    position = (25,25)
    index_of_directions_to_try_offset[position] = 0
    index_of_directions_to_try[position] = 0
    the_result = -1
    op = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
    while True:
        layout[position] = 0 # already seen
        direction = find_next_direction(layout, index_of_directions_to_try, index_of_directions_to_try_offset, position, ordered_directions_map[ilayout])
        op.input([direction])
        the_result = op.run()
        print(position, direction, the_result)
        if the_result == 2:
            position = update_position(direction, position)
            layout[position] = 2
            break
        elif the_result == 1:
            newstate = (position[0], position[1], direction)
            # if newstate in states:
            #     assert(1==0)
            # else:
            #     states.add(newstate)
            position = update_position(direction, position)
            update_attempted_directions(direction, position, index_of_directions_to_try_offset, ordered_directions_map[ilayout])
        elif the_result == 0:
            put_wall_in_direction(direction, position, layout)
    layouts[ilayout,:,:] = layout

uberlayout = layouts[0,:,:]
for ilayout in range(1,len(ordered_directions_map)):
    for ii in range(51):
        for jj in range(51):
            if uberlayout[ii,jj] == -1 and layouts[ilayout,ii,jj] != -1:
                uberlayout[ii,jj] = layouts[ilayout,ii,jj]

# flood fill time!
# nah it's not cyclic so just do a tree
# from any spot, you find all adjacent guys whose distances are't in the distance dict
# for each one, set its distance equal to one more and then recurrence it
position = (25,25)
distances = {position: 0}
def find_distance_from_all_points(position):
    adjacent_positions = [update_position(direction, position) for direction in [1,2,3,4]]
    valid_adjacent_positions = []
    for potential_valid_position in adjacent_positions:
        if (
            potential_valid_position[0] >= 0 and
            potential_valid_position[0] < 51 and
            potential_valid_position[1] >= 0 and
            potential_valid_position[1] < 51 and
            uberlayout[potential_valid_position] != 1 and
            potential_valid_position not in distances
        ):
            valid_adjacent_positions.append(potential_valid_position)
    for newposition in valid_adjacent_positions:
        distances[newposition] = distances[position] + 1
        find_distance_from_all_points(newposition)

find_distance_from_all_points(position)

position = (7,7)
distances = {position: 0}
def find_distance_from_all_points(position):
    adjacent_positions = [update_position(direction, position) for direction in [1,2,3,4]]
    valid_adjacent_positions = []
    for potential_valid_position in adjacent_positions:
        if (
            potential_valid_position[0] >= 0 and
            potential_valid_position[0] < 51 and
            potential_valid_position[1] >= 0 and
            potential_valid_position[1] < 51 and
            uberlayout[potential_valid_position] == 0 and
            potential_valid_position not in distances
        ):
            valid_adjacent_positions.append(potential_valid_position)
    for newposition in valid_adjacent_positions:
        distances[newposition] = distances[position] + 1
        find_distance_from_all_points(newposition)

find_distance_from_all_points(position)

maxdist = 0
for position in distances:
    if distances[position] > maxdist:
        maxpos = position
        maxdist = distances[position]
