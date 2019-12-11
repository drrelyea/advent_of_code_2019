# we might want to be able to assess the state of a VM
# the input codes might all be linked
# omg they might want a rewind capability... AAAAAAA

from opcode_computer import opcode_computer

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = inpstring[0].strip()
amplist = inpstring.split(',')
amplist = [int(a) for a in amplist]

amplist_orig = copy(amplist)

thegrid = np.zeros((510,510),dtype=int)
thepos = (250,250)
facing = (0,1)
facingdict = {
    (0,1,0): (-1,0),
    (0,1,1): (1,0),
    (0,-1,0): (1,0),
    (0,-1,1): (-1,0),
    (1,0,0): (0,1),
    (1,0,1): (0,-1),
    (-1,0,0): (0,-1),
    (-1,0,1): (0,1)
}
op = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
position_set = set()
numvisited = 0
thegrid[thepos] = 1
while 1:
    op.input([thegrid[thepos]])
    color = op.run()
    if type(color) != np.int64:
        break
    direction = op.run()
    # print(numvisited, thepos, thegrid[thepos], color, direction, facing)
    position_set.add(thepos)
    thegrid[thepos] = color
    facingkey = facing + (direction,)
    facing = facingdict[facingkey]
    thepos = (thepos[0] + facing[0], thepos[1] + facing[1])
imshow(thegrid[245:300,260:240:-1].T,aspect='auto')