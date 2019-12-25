import numpy as np
with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()


newstring = []
for tile in inpstring:
    newstring.append([aa for aa in tile.strip('\n')])

aa = np.array(newstring)
Nx = aa.shape[0]
Ny = aa.shape[1]
def find_n_adjacent(aa,ii,jj):
    nadj = 0
    if ii > 0:
        nadj += aa[ii-1,jj] == '#'
    if ii < Nx - 1:
        nadj += aa[ii+1,jj] == '#'
    if jj > 0:
        nadj += aa[ii,jj-1] == '#'
    if jj < Ny - 1:
        nadj += aa[ii,jj+1] == '#'
    return nadj

# themap = {
#     (0,0): [(0,1,0),(1,0,0),(1,2,1),(2,1,1)],
#     (0,1): [(0,0,0),(0,2,0),(1,1,0),(2,1,1)],
#     (0,2): [(0,1,0),(0,3,0),(1,2,0),(2,1,1)],
#     (0,3): [(0,2,0),(0,4,0),(1,3,0),(2,1,1)],
#     (0,4): [(0,3,0),(1,4,0),(3,2,1),(2,1,1)],
#     (1,0): [(0,0,0),(2,0,0),(1,1,0),(1,2,1)],
#     (1,1): [(0,1,0),(1,0,0),(1,2,0),(2,1,0)],
#     (1,2): [(0,2,0),(1,1,0),(1,3,0),(0,0,-1),(0,1,-1),(0,2,-1),(0,3,-1),(0,4,-1)],
#     (1,3): [(0,3,0),(1,2,0),(1,4,0),(2,3,0)],
#     (1,4): [(0,4,0),(2,4,0),(1,3,0),(3,2,1)],
#     (2,0): [(1,0,0),(3,0,0),(2,1,0),(1,2,1)],
#     (2,1): [(1,1,0),(2,0,0),(3,1,0),(0,0,-1),(1,0,-1),(2,0,-1),(3,0,-1),(4,0,-1)],
#     (2,3): [(1,3,0),(2,4,0),(3,3,0),(0,0,-1),(0,1,-1),(0,2,-1),(0,3,-1),(0,4,-1)],
#     (2,4): [(1,4,0),(3,4,0),(2,3,0),(3,2,1)],
#     (3,0): [(2,0,0),(4,0,0),(3,1,0),(1,2,1)],
#     (3,1): [(2,1,0),(3,0,0),(3,2,0),(4,1,0)],
#     (3,2): [(3,1,0),(3,3,0),(4,2,0),(0,0,-1),(0,1,-1),(0,2,-1),(0,3,-1),(0,4,-1)],
#     (3,3): [(2,3,0),(4,3,0),(3,2,0),(3,4,0)],
#     (3,4): [(2,4,0),(4,4,0),(3,3,0),(3,2,0)],
#     (4,0): [(4,1,0),(3,0,0),(1,2,1),(2,3,1)],
#     (4,1): [(4,0,0),(4,2,0),(3,1,0),(2,3,1)],
#     (4,2): [(4,1,0),(4,3,0),(3,2,0),(2,3,1)],
#     (4,3): [(4,2,0),(4,4,0),(3,3,0),(2,3,1)],
#     (4,4): [(4,3,0),(1,4,0),(3,2,1),(2,3,1)]
# }
kk = 200
NN = 2*kk +1

def find_n_adjacent_3d(aa,depth,ii,jj):
    nadj = 0
    thelist = [(ii-1,jj),(ii+1,jj),(ii,jj-1),(ii,jj+1)]
    newlist = []
    for item in thelist:
        if item[0] < 0:
            newlist.append((depth+1,1,2))
        elif item[0] > 4:
            newlist.append((depth+1,3,2))
        elif item[1] < 0:
            newlist.append((depth+1,2,1))
        elif item[1] > 4:
            newlist.append((depth+1,2,3))
        elif item == (2,2):
            if ii == 2:
                if jj == 1:
                    newlist+=[(depth-1,0,0),(depth-1,1,0),(depth-1,2,0),(depth-1,3,0),(depth-1,4,0)]
                if jj == 3:
                    newlist+=[(depth-1,0,4),(depth-1,1,4),(depth-1,2,4),(depth-1,3,4),(depth-1,4,4)]
            if jj == 2:
                if ii == 1:
                    newlist+=[(depth-1,0,0),(depth-1,0,1),(depth-1,0,2),(depth-1,0,3),(depth-1,0,4)]
                if ii == 3:
                    newlist+=[(depth-1,4,0),(depth-1,4,1),(depth-1,4,2),(depth-1,4,3),(depth-1,4,4)]
        else:
            newlist.append((depth,item[0],item[1]))

    for item in newlist:
        if item[0] >= 0 and item[0] < NN:
            # print((depth + pos[2],ii,jj))
            nadj += aa[item]
    return nadj

# ss = set()
# while 1:
#     bb = aa.copy()
#     for ii in range(5):
#         for jj in range(5):
#             Nadj = find_n_adjacent(aa,ii,jj)
#             if aa[ii,jj] == '#' and Nadj != 1:
#                 bb[ii,jj] = '.'
#             elif aa[ii,jj] == '.' and (Nadj == 1 or Nadj == 2):
#                 bb[ii,jj] = '#'
#             else:
#                 bb[ii,jj] = aa[ii,jj]
#     aa = bb.copy()
#     print(aa)
#     aalist = []
#     for ii in range(5):
#         aalist += list(aa[ii,:])
#     aawhere = ''.join(qq for qq in aalist)
#     if aawhere in ss:
#         print('HERE')
#         break
#     ss.add(aawhere)

# bio = 0
# for ii in range(5):
#     for jj in range(5):
#         if aa[ii,jj] == '#':
#             bio += 2**(jj + ii*5)


kk = 200
NN = 2*kk +1
aahash = np.zeros((NN,5,5),dtype = '<U1')
ppp = np.array(newstring)
aahash[kk,:,:] = ppp
aa = np.zeros((NN,5,5))
aa[aahash == '#'] = 1
for iloop in range(200):
    print(iloop)
    bb = aa.copy()
    for depth in range(aa.shape[0]):
        for ii in range(5):
            for jj in range(5):
                if ii == 2 and jj == 2:
                    continue
                Nadj = find_n_adjacent_3d(aa,depth,ii,jj)
                if aa[depth,ii,jj] == 1 and Nadj != 1:
                    bb[depth,ii,jj] = 0
                elif aa[depth,ii,jj] == 0 and (Nadj == 1 or Nadj == 2):
                    bb[depth,ii,jj] = 1
                else:
                    bb[depth,ii,jj] = aa[depth,ii,jj]
    aa = bb.copy()
