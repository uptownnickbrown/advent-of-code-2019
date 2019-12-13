from IntcodeComputer import *

def chunkify_output(l, size):
    return [l[i:i+size] for i, val in enumerate(l) if i % size == 0]

raw_input = [int(address) for address in open('input.txt', 'r').read().split(',')]
computer = Computer(raw_input)
computer.run_program()
tiles = chunkify_output(computer.outputs,3)

print('Answer 1')
print(sum([1 for tile in tiles if tile[2] == 2]))