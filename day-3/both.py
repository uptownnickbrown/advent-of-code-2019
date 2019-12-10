import re
from operator import attrgetter, itemgetter
from collections import defaultdict

class Step:
    def __init__(self, step):
        regex = '([RLDU])(\d+)'
        (self.direction, distance) = re.findall(regex,step)[0]
        self.distance = int(distance)

    def __repr__(self):
        return f'Go {self.distance} steps in {self.direction} direction.'

class Wire:
    def __init__(self, steps):
        self.steps = [Step(step.strip()) for step in steps.split(',')]

    def __repr__(self):
        return f'{self.steps}'

def draw_step(grid,x,y,end,char,this_wire):
    if (x,y) in grid:
        # already in the grid, already a cross, leave it a cross
        if grid[(x,y)][0] == 'X':
            pass
        # already in the grid but _not_ a cross yet, check if it's in the grid from this wire or not
        elif (x,y) in this_wire:
            grid[(x,y)] = (char, len(this_wire) + 1)
        else:
            grid[(x,y)] = ('X', grid[(x,y)][1] + len(this_wire) + 1)
    elif end:
        grid[(x,y)] = ('+', len(this_wire) + 1)
    else:
        grid[(x,y)] = (char, len(this_wire) + 1)

class Grid:
    def __init__(self):
        self.grid = {}
        self.grid[(0,0)] = ('o',0)

    def add_wire(self, wire):
        x = 0
        y = 0
        this_wire = []
        for step in wire.steps:
            if step.direction == 'R':
                for i in range(step.distance):
                    x = x + 1
                    draw_step(self.grid, x, y, i == step.distance - 1, '-', this_wire)
                    this_wire.append((x,y))
            elif step.direction == 'L':
                for i in range(step.distance):
                    x = x - 1
                    draw_step(self.grid, x, y, i == step.distance - 1, '-', this_wire)
                    this_wire.append((x,y))
            elif step.direction == 'U':
                for i in range(step.distance):
                    y = y + 1
                    draw_step(self.grid, x, y, i == step.distance - 1, '|', this_wire)
                    this_wire.append((x,y))
            elif step.direction == 'D':
                for i in range(step.distance):
                    y = y - 1
                    draw_step(self.grid, x, y, i == step.distance - 1, '|', this_wire)
                    this_wire.append((x,y))

    def find_min_cross_manhattan(self):
        crosses = [key for (key,val) in self.grid.items() if val[0] == 'X']
        return min([abs(x) + abs(y) for (x,y) in crosses])

    def find_min_cross_step_count(self):
        crosses = [(key,val) for (key,val) in self.grid.items() if val[0] == 'X']
        return min([val[1] for (key,val) in crosses])

    def __repr__(self):
        keys = self.grid.keys()
        x_keys = [x for (x,y) in keys]
        y_keys = [y for (x,y) in keys]
        x_min = min(x_keys)
        x_max = max(x_keys)
        y_min = min(y_keys)
        y_max = max(y_keys)
        rows = []
        for y in reversed(range(y_min - 1,y_max + 2)):
            row = ''
            for x in range(x_min - 1, x_max + 2):
                if (x,y) in self.grid:
                    row = row + self.grid[(x,y)][0]
                else:
                    row = row + '.'
            rows.append(row)
        return '\n'.join(rows)

wires = [Wire(l) for l in open('input.txt','r').readlines()]
grid = Grid()
for wire in wires:
    grid.add_wire(wire)
# open('out.txt','w').write(grid.__repr__())

# report results
print ('Answer 1:')
print (grid.find_min_cross_manhattan())

#report results
print ('Answer 2:')
print (grid.find_min_cross_step_count())