from IntcodeComputer import *
import time

def print_tile(id):
    if id == 0:
        return ' '
    if id == 1:
        return '|'
    if id == 2:
        return '█'
    if id == 3:
        return '='
    if id == 4:
        return '.'

class Game:
    def __init__(self):
        self.coords = {}
        self.score = 0
        self.ball_y_v = 1
        self.ball_x_v = 0
        self.ball_x = 19
        self.ball_y = 16
        self.paddle_x = 21
        self.paddle_move = 0

    def __repr__(self):
        keys = self.coords.keys()
        x_keys = [x for (x,y) in keys]
        y_keys = [y for (x,y) in keys]
        x_min = min(x_keys)
        x_max = max(x_keys)
        y_min = min(y_keys)
        y_max = max(y_keys)
        rows = []
        for y in range(y_min - 2,y_max + 3):
            row = ''
            for x in range(x_min - 2, x_max + 3):
                if (x,y) in self.coords:
                    row = row + print_tile(self.coords[(x,y)])
                else:
                    row = row + ' '
            rows.append(row)
        return '\n'.join(rows)

def chunkify_output(l, size):
    return [l[i:i+size] for i, val in enumerate(l) if i % size == 0]

raw_input = [int(address) for address in open('input.txt', 'r').read().split(',')]
computer = Computer(raw_input)
computer.run_program()
tiles = chunkify_output(computer.outputs,3)

print('Answer 1')
print(sum([1 for tile in tiles if tile[2] == 2]))

def initialize_game(computer, game):
    tiles = chunkify_output(computer.outputs, 3)
    computer.outputs = []
    for tile in tiles:
        (x, y, id) = tile
        game.coords[(x, y)] = id

def output_to_game(computer, game):
    tiles = chunkify_output(computer.outputs, 3)
    computer.outputs = []
    for tile in tiles:
        (x, y, id) = tile
        if (x, y) == (-1, 0):
            game.score = id
        else:
            game.coords[(x, y)] = id
            if id == 3:
                game.paddle_x = x
            if id == 4:
                (game.ball_x_v, game.ball_y_v) = (x - game.ball_x, y - game.ball_y)
                (game.ball_x, game.ball_y) = (x,y)

                # going down - paddle at y = 18
                if game.ball_y_v > 0:
                    time_to_hit = (18 - game.ball_y) / game.ball_y_v
                    projected_hit_x = game.ball_x + time_to_hit * game.ball_x_v
                    game.paddle_move = projected_hit_x - game.paddle_x
                else:
                    game.paddle_move = game.ball_x_v

def run_step():
    input = 0
    if game.paddle_move > 0:
        input = 1
    elif game.paddle_move < 0:
        input = -1
    computer.run_to_pause(inputs=[input])
    output_to_game(computer, game)

raw_input[0] = 2
computer = Computer(raw_input)
game = Game()

computer.run_to_pause()
initialize_game(computer, game)

i = 0
while computer.complete == False:
    run_step()
    # just for a pretty animated terminal output :)
    i += 1
    if i < 100:
        print(game)
        time.sleep(0.04)
    elif i < 1200 and i % 5 == 0:
        print(game)
        time.sleep(0.03)
    elif i < 6000 and i % 20 == 0:
        print(game)
        time.sleep(0.03)
    elif i % 30 == 0:
        print(game)
        time.sleep(0.02)

print('Answer 2:')
print(game.score)