import numpy as np

with open('/Users/relyea/data/input.txt') as input_file:
    inpstring = input_file.readlines()

# once you have those, for every period, find all paths to all other periods using bloop
# then just do a simple traversal, but if you find a loop, throw it out

themaze_list = []
for iline, line in enumerate(inpstring):
    newline = [a for a in line.strip('\n')]
    themaze_list.append(newline)

themaze = np.array(themaze_list)

y1 = 2
y2 = themaze.shape[1] - 3
x1 = 2
x2 = themaze.shape[0] - 3

boundary_points_to_names = {}
boundary_names_to_points = {}

def fill_exit_dicts(point, name, edge):
    boundary_points_to_names[point] = (name, edge)
    if name not in boundary_names_to_points:
        boundary_names_to_points[name] = [(point, edge)]
    else:
        boundary_names_to_points[name].append((point, edge))
    return

INNER = 1
OUTER = 0

for ii in range(x1, x2+1):
    if themaze[ii, y1] == '.':
        point = (ii, y1)
        name = ''.join(themaze[ii, 0:2])
        fill_exit_dicts(point, name, OUTER)
    if themaze[ii, y2] == '.':
        point = (ii, y2)
        name = ''.join(themaze[ii, y2+1:])
        fill_exit_dicts(point, name, OUTER)
for jj in range(y1, y2+1):
    if themaze[x1, jj] == '.':
        point = (x1, jj)
        name = ''.join(themaze[0:2, jj])
        fill_exit_dicts(point, name, OUTER)
    if themaze[x2, jj] == '.':
        point = (x2, jj)
        name = ''.join(themaze[x2+1:, jj])
        fill_exit_dicts(point, name, OUTER)

space_coords = np.where(themaze[2:-2,2:-2] == ' ')
x3 = space_coords[0][0]+2
x4 = space_coords[0][-1]+2
y3 = space_coords[1][0]+2
y4 = space_coords[1][-1]+2

for ii in range(x3,x4):
    if themaze[ii, y3-1] == '.':
        point = (ii, y3-1)
        name = ''.join(themaze[ii, y3:y3+2])
        fill_exit_dicts(point, name, INNER)
    if themaze[ii, y4+1] == '.':
        point = (ii, y4+1)
        name = ''.join(themaze[ii, y4-1:y4+1])
        fill_exit_dicts(point, name, INNER)
for jj in range(y3,y4):
    if themaze[x3-1, jj] == '.':
        point = (x3-1, jj)
        name = ''.join(themaze[x3:x3+2, jj])
        fill_exit_dicts(point, name, INNER)
    if themaze[x4+1, jj] == '.':
        point = (x4+1, jj)
        name = ''.join(themaze[x4-1:x4+1, jj])
        fill_exit_dicts(point, name, INNER)

def get_neighbors(point):
    return [(point[0],point[1]+1),(point[0],point[1]-1),(point[0]-1,point[1]),(point[0]+1,point[1])]

def is_in_maze(point):
    if (
        point[0] < x1 or 
        point[0] > x2 or
        point[1] < y1 or
        point[1] > y2
    ):
        return False
    else:
        return True

point_to_point_distance_map = {}
for entrancepoint in boundary_points_to_names:
    (entrancename, entranceedge) = boundary_points_to_names[entrancepoint]
    # print(entrancename)
    if (entrancename, entranceedge) not in point_to_point_distance_map:
        point_to_point_distance_map[(entrancename, entranceedge)] = []
    slurm_list = [entrancepoint]
    totaldistance = 0
    current_iteration = [entrancepoint]
    while current_iteration != []:
        new_current_iteration = []
        totaldistance += 1
        # print(totaldistance)
        for point in current_iteration:
            neighbors = get_neighbors(point)
            valid_neighbors = [neighbor for neighbor in neighbors if is_in_maze(neighbor) and themaze[neighbor] == '.' and neighbor not in slurm_list]
            for neighbor in valid_neighbors:
                slurm_list.append(neighbor)
                new_current_iteration.append(neighbor)
                if neighbor in boundary_points_to_names:
                    (name, edge) = boundary_points_to_names[neighbor]
                    point_to_point_distance_map[(entrancename, entranceedge)].append([name,edge,totaldistance])
        current_iteration = new_current_iteration


start = 'AA'
def find_distance_to_neighbors(distance, point, edge, layer, points_already_visited):
    current_best = 10000
    current_found = False
    best_points_visited = []
    # print(distance, point, edge, layer, points_already_visited, 'START')
    for (neighbor,newedge,newdistance) in point_to_point_distance_map[(point,edge)]:
        # print(neighbor, newedge, newdistance,'NEIGHBOR')
        if neighbor == 'AA':
            continue
        elif neighbor == 'ZZ':
            if layer != 0:
                continue
            else:
                if distance + newdistance < current_best:
                    return True, distance + newdistance, points_already_visited
        elif layer == 0 and newedge == OUTER:
            continue
        elif (neighbor, layer) not in points_already_visited:
            if newedge == INNER:
                newlayer = layer + 1
                if newlayer > 30:
                    continue
            else:
                newlayer = layer - 1
                if newlayer < 0:
                    continue
            wasfound, found_distance, visitlist = find_distance_to_neighbors(distance + newdistance + 1, neighbor, 1-newedge, newlayer, points_already_visited + [(neighbor, layer)])
            if wasfound and found_distance < current_best:
                current_best = found_distance
                current_found = True
                best_points_visited = visitlist
    return current_found, current_best, best_points_visited

find_distance_to_neighbors(0, 'AA', OUTER, 0, [])
