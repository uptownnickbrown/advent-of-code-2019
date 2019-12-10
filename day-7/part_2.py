from itertools import permutations
from IntcodeComputer import *

raw_input = [int(address) for address in open('input.txt','r').read().split(',')]

highest_output = 0
for phase_setting in permutations(range(5,10)):
    computers = [Computer(raw_input) for i in range(5)]
    for i, computer in enumerate(computers):
        computer.run_to_pause(inputs=[phase_setting[i]])

    last_output = 0
    active_ix = 0
    while any([computer.complete != True]):
        active = computers[active_ix % 5]
        active.run_to_pause(inputs=[last_output])
        last_output = active.outputs[-1]
        active_ix += 1

    if last_output > highest_output:
        highest_output = last_output

print(f'Answer 2: {highest_output}')