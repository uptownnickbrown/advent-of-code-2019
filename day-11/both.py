from itertools import permutations
from IntcodeComputer import *

def print_coord(color_val):
    if color_val == 0:
        return '.'
    if color_val == 1:
        return '#'

class Robot:
    def __init__(self, grid):
        self.heading = 0 # 0 = up
        self._position = {'x':0,'y':0}
        self.on = grid

    def position(self):
        return (self._position['x'], self._position['y'])

    def turn(self, instruction):
        if instruction == 0:
            degrees = -90
        elif instruction == 1:
            degrees = 90
        self.heading = self.heading + degrees
        if self.heading < 0:
            self.heading += 360
        self.heading = self.heading % 360

    def move(self):
        if self.heading == 0:
            self._position['y'] = self._position['y'] + 1
        if self.heading == 90:
            self._position['x'] = self._position['x'] + 1
        if self.heading == 180:
            self._position['y'] = self._position['y'] - 1
        if self.heading == 270:
            self._position['x'] = self._position['x'] - 1
        if self.position() not in self.on.coords:
            self.on.coords[self.position()] = 0

    def paint(self, instruction):
        self.on.coords[self.position()] = instruction

    def __repr__(self):
        if self.heading == 0:
            return '^'
        if self.heading == 90:
            return '>'
        if self.heading == 180:
            return 'v'
        if self.heading == 270:
           return '<'


class Grid:
    def __init__(self):
        self.coords = {}
        self.coords[(0,0)] = 0
        self.robot = Robot(self)

    def __repr__(self):
        keys = self.coords.keys()
        x_keys = [x for (x,y) in keys]
        y_keys = [y for (x,y) in keys]
        x_min = min(x_keys)
        x_max = max(x_keys)
        y_min = min(y_keys)
        y_max = max(y_keys)
        rows = []
        for y in reversed(range(y_min - 2,y_max + 3)):
            row = ''
            for x in range(x_min - 2, x_max + 3):
                if (x, y) == self.robot.position():
                    row = row + str(self.robot)
                else:
                    if (x,y) in self.coords:
                        row = row + print_coord(self.coords[(x,y)])
                    else:
                        row = row + print_coord(0)
            rows.append(row)
        return '\n'.join(rows)

computer = Computer([int(address) for address in open('input.txt', 'r').read().split(',')])
grid = Grid()

def paint_turn_move(outputs):
    grid.robot.paint(outputs[0])
    grid.robot.turn(outputs[1])
    grid.robot.move()

while computer.complete == False:
    on = grid.coords[grid.robot.position()]
    computer.run_to_pause(inputs=[on])
    paint_turn_move(computer.outputs[-2:])

print('Answer 1:')
print(len(grid.coords))

print('Answer 2:')

