# we might want to be able to assess the state of a VM
# the input codes might all be linked
# omg they might want a rewind capability... AAAAAAA

import numpy as np

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

norbs = len(inpstring)

pos = np.zeros((norbs, 3))
vel = np.zeros((norbs, 3))

for iline, line in enumerate(inpstring):
    pos[iline, 0] = line.split(',')[0].split('=')[1]
    pos[iline, 1] = line.split(',')[1].split('=')[1]
    pos[iline, 2] = line.split(',')[2].split('=')[1].split('>')[0]

ntimesteps = 10
ke = np.zeros((norbs, ntimesteps))
pe = np.zeros((norbs, ntimesteps))


for timestep in range(ntimesteps):
    print(pos)
    print(vel)
    ke[:, ii] = np.sum(np.abs(vel), axis=1)
    pe[:, ii] = np.sum(np.abs(pos), axis=1)
    # energy = np.sum(np.abs(pos), axis=1) * np.sum(np.abs(vel), axis=1)
    print(ke[:, ii])
    print(pe[:, ii])
    print(sum(ke[:, ii]))
    print(prod(ke[:, ii]))
    for ii in range(norbs):
        for jj in range(ii+1, norbs):
            for xyz in range(3):
                vel[ii, xyz] += np.sign(pos[jj, xyz] - pos[ii, xyz])
                vel[jj, xyz] -= np.sign(pos[jj, xyz] - pos[ii, xyz])


        for xyz in range(3):
            pos[ii, xyz] += vel[ii, xyz]


def find_n_steps(vect):
    vel = vect * 0
    newvect = copy(vect)
    nsteps = 0
    notfirst = False
    vellist = np.zeros((1000000,norbs))
    while not (
        prod(newvect == vect) and notfirst
    ):
        notfirst = True
        nsteps += 1
        for iorb in range(norbs):
            vel[iorb] += sum(newvect > newvect[iorb]) - sum(newvect < newvect[iorb])
        vellist[nsteps,:] = vel
        newvect += vel
    return nsteps + 1, vellist

#  4686774924 / 2351 / 983 / 13 / 3 / 2 / 13 / 2

pos = np.zeros((norbs, 3))
vel = np.zeros((norbs, 3))

for iline, line in enumerate(inpstring):
    pos[iline, 0] = line.split(',')[0].split('=')[1]
    pos[iline, 1] = line.split(',')[1].split('=')[1]
    pos[iline, 2] = line.split(',')[2].split('=')[1].split('>')[0]

nsteparray = zeros(3)
for axis in range(3):
    print(axis)
    nsteparray[axis] = find_n_steps(copy(pos[:,axis]))

In [153]: [bb for bb in aa if nsteparray[0] % bb == 0]
Out[153]: [2, 40357]

In [154]: [bb for bb in aa if nsteparray[1] % bb == 0]
Out[154]: [2, 115807]

In [155]: [bb for bb in aa if nsteparray[2] % bb == 0]
Out[155]: [2, 25589]

40357 * 115807 * 25589 * 2