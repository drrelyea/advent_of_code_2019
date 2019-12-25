import numpy as np

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

newinpstring = []
for line in inpstring:
    newinpstring.append(line.strip())
# inpstring = ['19617804207202209144916044189917']

for irow,row in enumerate(newinpstring):
    for jcol,col in enumerate(row):
        if col == '@':
            startrow, startcol = irow, icol

ilen = len(newinpstring)
jlen = len(newinpstring[0])

def get_adjacency_map(newinpstring):
    adjacency_map = {}
    for ii in range(0,ilen):
        for jj in range(0, jlen):
            for ipm in range(ii-1,ii+2):
                jpm = jj
                if (
                    ipm >= 0 and
                    jpm >= 0 and
                    ipm < ilen and
                    jpm < jlen and
                    newinpstring[ipm][jpm] != '#' and
                    not (ipm,jpm) == (ii,jj)
                ):
                    if (ii,jj) not in adjacency_map:
                        adjacency_map[(ii,jj)] = [(ipm,jpm)]
                    else:
                        adjacency_map[(ii,jj)].append((ipm,jpm))
            for jpm in range(jj-1, jj+2):
                ipm = ii
                if (
                    ipm >= 0 and
                    jpm >= 0 and
                    ipm < ilen and
                    jpm < jlen and
                    newinpstring[ipm][jpm] != '#' and
                    not (ipm,jpm) == (ii,jj)
                ):
                    if (ii,jj) not in adjacency_map:
                        adjacency_map[(ii,jj)] = [(ipm,jpm)]
                    else:
                        adjacency_map[(ii,jj)].append((ipm,jpm))
    return adjacency_map

themap = get_adjacency_map(newinpstring)

doorlist = 'QWERTYUIOPASDFGHJKLZXCVBNM'
keylist  = 'qwertyuiopasdfghjklzxcvbnm'

keyposdict = {}
for irow,row in enumerate(newinpstring):
    print(row)
    for jcol,col in enumerate(row):
        if col in keylist:
            keyposdict[col] = (irow, jcol)


ok hold it
if a key is in a dead end, you want to get it as soon as you are closest to it (including now)
if only one key is free to open a door, get it now




key_distance = {}
def slurm_out(key_start, key_sought):
    keyFound = False
    wall_list = []
    pointlist = [keyposdict[key_start]]
    already_visited_list = []
    doors_hit = []
    iteration = 0
    while not keyFound:
        actual_new_points = []
        iteration += 1
        for currentpoint in pointlist:
            adjacent_points = themap[currentpoint]
            for point in adjacent_points:
                if point not in already_visited_list:
                    actual_new_points.append(point)
                    already_visited_list.append(point)
                    if newinpstring[point[0]][point[1]] in doorlist:
                        doors_hit.append(newinpstring[point[0]][point[1]])
                    elif newinpstring[point[0]][point[1]] == key_sought:
                        key_distance[(key_start, key_sought)] = (iteration, doors_hit)
                        keyFound = True
                        return
        pointlist = list(actual_new_points)



distance is simple - just a slurm function where you get the set of all squares and then the set of all adjacent squares
you then take every path of step 2, 3, 4, 5, 6, etc


ok so the idea is
figure out the distance from each key to every other key (no doors), along with the start to every key not behind a door
store that, along with the doors needed to go through to traverse that
it is N^2 - you should go from every key to every other key in order
if a door in in the way and you don't have that key, make the number large


