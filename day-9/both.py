from itertools import permutations
from IntcodeComputer import *

raw_input = [int(address) for address in open('input.txt', 'r').read().split(',')]

print('Answer 1:')
print(Computer(raw_input).run_program(inputs=[1]))

print('Answer 2:')
print(Computer(raw_input).run_program(inputs=[2]))
