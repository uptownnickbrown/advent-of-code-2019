from itertools import permutations
from IntcodeComputer import *

raw_input = [int(address) for address in open('input.txt','r').read().split(',')]

highest_output = 0
for phase_setting in permutations(range(5)):
    computers = [Computer(raw_input) for i in range(5)]
    last_output = 0
    for i, computer in enumerate(computers):
        computer.run_program(inputs=[phase_setting[i], last_output])
        last_output = computer.outputs[-1]
    if last_output > highest_output:
        highest_output = last_output

print(f'Answer 1: {highest_output}')
