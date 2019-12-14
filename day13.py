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

# op = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
# tilenum = 0
# ballpos = [0,0]
# while 1:
#     # op.input([thegrid[thepos]])
#     xpos = op.run()
#     if type(xpos) != np.int64:
#         break
#     ypos = op.run()
#     tileid = op.run()
#     if tileid == 2:
#         tilenum += 1
#     if tileid == 4:
#         ballpos = []

blocks = []
walls = []
op = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
tilenum = 0
ballpos = [0,0]
while 1:
    # op.input([thegrid[thepos]])
    xpos = op.run()
    if type(xpos) != np.int64:
        break
    ypos = op.run()
    tileid = op.run()
    if tileid == 2:
        tilenum += 1
        blocks.append((xpos, ypos))
    if tileid == 1:
        walls.append((xpos, ypos))
    if tileid == 4:
        ballpos = []

amplist_orig[0] = 2
op = opcode_computer(list(copy(list(amplist_orig)))+[0]*100000)
tilenum = 0
ballformerpos = [0,0]
ballpos = [0,0]
paddlepos = [0,0]
score = 0
movepaddle = 2
op.input([0])
nballsteps = 0
paddle_or_ball = 'ball'
while 1:
    # op.input([thegrid[thepos]])
    xpos = op.run()
    if type(xpos) != np.int64:
        break
    ypos = op.run()
    tileid = op.run()
    if xpos == -1 and ypos == 0:
        score = tileid
        print('SCORE', score)
        continue
    if tileid == 2:
        # print('BLOCK', xpos, ypos)
        tilenum += 1
    if tileid == 1:
        # print('WALL', xpos, ypos)
        tilenum += 1
    elif tileid == 4:
        ballformerpos = [ballpos[0],ballpos[1]]
        ballpos = [xpos,ypos]
        xdiff = ballpos[0] - ballformerpos[0]
        ydiff = ballpos[1] - ballformerpos[1]
        print('BALL', ballpos)
        # print('DIFF', xdiff, ydiff)
        paddle_or_ball == 'ball'
        nballsteps += 1
        # if nballsteps > 1:
        #     if (ballpos[0] + xdiff, ballpos[1] + ydiff) in walls:
        #         pass
        #     print('PB', ballpos[0] + xdiff, paddlepos[0])
        #     if ballpos[0] + xdiff > paddlepos[0]:
        #         print('1')
        #         op.input([1])
        #     elif ballpos[0] + xdiff < paddlepos[0]:
        #         print('-1')
        #         op.input([-1])
        #     else:
        #         print('0')
        #         op.input([0])
    elif tileid == 3:
        paddlepos = [xpos,ypos]
        print('PADDLE', paddlepos)
        paddle_or_ball == 'paddle'
    if tileid == 3 or tileid == 4:
        if ballpos[0] > paddlepos[0]:
            print('1')
            op.input_no_changes([1])
        elif ballpos[0] < paddlepos[0]:
            print('-1')
            op.input_no_changes([-1])
        else:
            print('0')
            op.input_no_changes([0])
    # if tileid == 3 or tileid == 4:

# wall is at 22 (21 is last spot)

# states are paddle left of ball, ball moving left, right
# paddle under ball, ball moving left, right

#     elif paddlepos[0] > ballpos[0]:
#         op.input(-1)
