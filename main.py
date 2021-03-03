from queue import Queue
from math import sqrt, floor

with open('./input.txt', 'r') as f:
    lines = f.readlines()
output_file = open('./output.txt', 'w')

method = lines[0].split()[0]
w, h = [int(x) for x in lines[1].split()]
start_x, start_y = [int(x) for x in lines[2].split()]
height_diff = int(lines[3].split()[0])
n = int(lines[4].split()[0])

target = []
for line in lines[5:5+n]:
    x, y = [int(x) for x in line.split()]
    target.append((x, y))

land = []
for line in lines[5+n:]:
    land.append([int(x) for x in line.split()])


class Node:
    def __init__(self, x, y, parent, path_cost, estimate=0):
        self.x = x
        self.y = y
        self.parent = parent
        self.path_cost = path_cost

        self.estimate = estimate
        self.desirability = path_cost+estimate


def output(node):
    path = []
    path.append((node.x, node.y))

    while(node.parent != None):
        node = node.parent
        path.append((node.x, node.y))

    for x, y in path[::-1]:
        output_file.write(str(x)+','+str(y)+' ')

    output_file.seek(output_file.tell()-1, 0)
    output_file.truncate()
    output_file.write('\n')

    print()


def BFS(target_x, target_y):
    start = Node(start_x, start_y, None, 0)
    q = Queue(-1)
    q.put(start)
    explored = set()

    while(not q.empty()):
        current = q.get()
        explored.add((current.x, current.y))

        current_height = abs(land[current.y][current.x]
                             ) if land[current.y][current.x] < 0 else 0
        next_locs = [(current.x-1, current.y-1), (current.x, current.y-1), (current.x+1, current.y-1),
                     (current.x-1, current.y), (current.x+1, current.y),
                     (current.x-1, current.y+1), (current.x, current.y+1), (current.x+1, current.y+1)]

        for (next_x, next_y) in next_locs:
            if (next_x < 0 or next_x > w-1) or (next_y < 0 or next_y > h-1):
                continue

            # check if it's explored
            if (next_x, next_y) in explored:
                continue

            next_height = abs(land[next_y][next_x]
                              ) if land[next_y][next_x] < 0 else 0
            next_cost = 1

            if abs(current_height-next_height) > height_diff:
                continue

            next_node = Node(next_x, next_y, current,
                             current.path_cost+next_cost)

            if next_x == target_x and next_y == target_y:
                output(next_node)
                return True

            q.put(next_node)

    # return failure
    return False


def UCS(target_x, target_y):
    start = Node(start_x, start_y, None, 0)
    l = []
    l.append(start)
    closed = []

    while(len(l)):
        current = l.pop()
        closed.append(current)

        if current.x == target_x and current.y == target_y:
            output(current)
            return True

        current_height = abs(land[current.y][current.x]
                             ) if land[current.y][current.x] < 0 else 0
        next_locs = [(current.x-1, current.y-1), (current.x, current.y-1), (current.x+1, current.y-1),
                     (current.x-1, current.y), (current.x+1, current.y),
                     (current.x-1, current.y+1), (current.x, current.y+1), (current.x+1, current.y+1)]

        for (next_x, next_y) in next_locs:
            if (next_x < 0 or next_x > w-1) or (next_y < 0 or next_y > h-1):
                continue

            next_height = abs(land[next_y][next_x]
                              ) if land[next_y][next_x] < 0 else 0
            if abs(current_height-next_height) > height_diff:
                continue

            next_cost = 14 if next_x != current.x and next_y != current.y else 10

            next_node = Node(next_x, next_y, current,
                             current.path_cost+next_cost)

            # if no node in open or closed has such state
            open_set = set([(node.x, node.y) for node in l])
            closed_set = set([(node.x, node.y) for node in closed])

            if (next_x, next_y) not in open_set and (next_x, next_y) not in closed_set:
                l.append(next_node)
            elif (next_x, next_y) in open_set:
                for i, node in enumerate(l):
                    if node.x == next_x and node.y == next_y and next_node.path_cost < node.path_cost:
                        del(l[i])
                        l.append(next_node)
            elif (next_x, next_y) in closed_set:
                for i, node in enumerate(closed):
                    if node.x == next_x and node.y == next_y and next_node.path_cost < node.path_cost:
                        del(closed[i])
                        l.append(next_node)

            l.sort(key=lambda x: x.path_cost, reverse=True)

    # return failure
    return False


def Astar(target_x, target_y):
    def h_func(start_x, start_y):
        return floor(10*sqrt((start_x-target_x)**2+(start_y-target_y)**2))

    start = Node(start_x, start_y, None, 0, h_func(start_x, start_y))
    l = []
    l.append(start)
    closed = []

    while(len(l)):
        current = l.pop()
        closed.append(current)

        if current.x == target_x and current.y == target_y:
            output(current)
            return True

        current_height = abs(land[current.y][current.x]
                             ) if land[current.y][current.x] < 0 else 0
        next_locs = [(current.x-1, current.y-1), (current.x, current.y-1), (current.x+1, current.y-1),
                     (current.x-1, current.y), (current.x+1, current.y),
                     (current.x-1, current.y+1), (current.x, current.y+1), (current.x+1, current.y+1)]

        for (next_x, next_y) in next_locs:
            if (next_x < 0 or next_x > w-1) or (next_y < 0 or next_y > h-1):
                continue

            next_height = abs(land[next_y][next_x]
                              ) if land[next_y][next_x] < 0 else 0
            if abs(current_height-next_height) > height_diff:
                continue

            move_cost = 14 if next_x != current.x and next_y != current.y else 10
            height_cost = abs(current_height-next_height)
            mud_level = land[next_y][next_x] if next_height == 0 else 0

            next_cost = move_cost+height_cost+mud_level

            next_node = Node(next_x, next_y, current,
                             current.path_cost+next_cost, h_func(next_x, next_y))

            # if no node in open or closed has such state
            open_set = set([(node.x, node.y) for node in l])
            closed_set = set([(node.x, node.y) for node in closed])

            if (next_x, next_y) not in open_set and (next_x, next_y) not in closed_set:
                l.append(next_node)
            elif (next_x, next_y) in open_set:
                for i, node in enumerate(l):
                    if node.x == next_x and node.y == next_y and next_node.desirability < node.desirability:
                        del(l[i])
                        l.append(next_node)
            elif (next_x, next_y) in closed_set:
                for i, node in enumerate(closed):
                    if node.x == next_x and node.y == next_y and next_node.desirability < node.desirability:
                        del(closed[i])
                        l.append(next_node)

            l.sort(key=lambda x: x.desirability, reverse=True)

    # return failure
    return False


if method == 'BFS':
    func = BFS
elif method == 'UCS':
    func = UCS
elif method == 'A*':
    func = Astar

for x, y in target:
    if not func(x, y):
        output_file.write('FAIL\n')

output_file.close()
