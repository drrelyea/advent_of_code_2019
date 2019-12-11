from fractions import Fraction
import numpy as np

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

inpstring = [aa.strip() for aa in inpstring]

asteroid_list = []
for ii in range(len(inpstring[0])):
    for jj in range(len(inpstring)):
        if inpstring[jj][ii] == '#':
            asteroid_list.append((ii,jj))

pairlist = {}
for aa in asteroid_list:
    pairlist[aa] = []
for ii in range(len(asteroid_list)-1):
    for jj in range(ii+1,len(asteroid_list)):
        asteroid = asteroid_list[ii]
        otherasteroid = asteroid_list[jj]
        xstep = otherasteroid[0] - asteroid[0]
        ystep = otherasteroid[1] - asteroid[1]
        if xstep == 0:
            pair = True
            for yy in range(asteroid[1]+1,otherasteroid[1]):
                if (asteroid[0], yy) in asteroid_list:
                    pair = False
                    break
            if pair == True:
                pairlist[asteroid].append(otherasteroid)
                pairlist[otherasteroid].append(asteroid)
            
        elif ystep == 0:
            pair = True
            for xx in range(asteroid[0]+1,otherasteroid[0]):
                if (xx, asteroid[1]) in asteroid_list:
                    pair = False
                    break
            if pair == True:
                pairlist[asteroid].append(otherasteroid)
                pairlist[otherasteroid].append(asteroid)

        else:
            thefraction = Fraction(xstep, ystep)
            x_it = np.abs(thefraction.numerator)*np.sign(xstep)
            y_it = np.abs(thefraction.denominator)*np.sign(ystep)
            nsteps = int(abs(xstep) / abs(x_it))
            pair = True
            for istep in range(1,nsteps):
                if (asteroid[0] + istep*x_it, asteroid[1] + istep*y_it) in asteroid_list:
                    pair = False
                    break
            if pair == True:
                pairlist[asteroid].append(otherasteroid)
                pairlist[otherasteroid].append(asteroid)
maxnum = 0
for pair in pairlist:
    # print(pair, len(pairlist[pair]))
    if len(pairlist[pair]) > maxnum:
        maxnum = len(pairlist[pair])
        print(pair)

asteroid_list = copy(orig_asteroid_list)
coords = (23,19)
index = asteroid_list.index(coords)
newpairlist = []
for ii in range(len(asteroid_list)):
    asteroid = coords
    otherasteroid = asteroid_list[ii]
    if otherasteroid == asteroid:
        continue
    xstep = otherasteroid[0] - asteroid[0]
    ystep = otherasteroid[1] - asteroid[1]
    if xstep == 0:
        y_it = np.sign(ystep)
        nsteps = int(abs(ystep) / abs(y_it))
        pair = True
        for istep in range(1,nsteps):
            if (asteroid[0], asteroid[1] + istep*y_it) in asteroid_list:
                pair = False
                break
        if pair == True:
            newpairlist.append(otherasteroid)
        
    elif ystep == 0:
        x_it = np.sign(xstep)
        nsteps = int(abs(xstep) / abs(x_it))
        pair = True
        for istep in range(1,nsteps):
            if (asteroid[0] + istep*x_it, asteroid[1]) in asteroid_list:
                pair = False
                break
        if pair == True:
            newpairlist.append(otherasteroid)

    else:
        thefraction = Fraction(xstep, ystep)
        x_it = np.abs(thefraction.numerator)*np.sign(xstep)
        y_it = np.abs(thefraction.denominator)*np.sign(ystep)
        nsteps = int(abs(xstep) / abs(x_it))
        pair = True
        for istep in range(1,nsteps):
            if (asteroid[0] + istep*x_it, asteroid[1] + istep*y_it) in asteroid_list:
                pair = False
                break
        if pair == True:
            newpairlist.append(otherasteroid)
    
pair_to_angle = []
for newasteroid in newpairlist:
    theangle = np.arctan2(newasteroid[0] - asteroid[0], newasteroid[1] - asteroid[1])
    pair_to_angle.append([theangle, newasteroid[0], newasteroid[1]])
pta = np.array(pair_to_angle)
indices = np.argsort(-pta[:,0])
