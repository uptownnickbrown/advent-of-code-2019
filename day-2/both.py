
def run_step(memory, pointer=0):
    instruction = memory[pointer]
    if instruction == 1:
        params = memory[pointer + 1:pointer + 4]
        memory[params[2]] = memory[params[0]] + memory[params[1]]
        return run_step(memory, pointer + 4)
    if instruction == 2:
        params = memory[pointer + 1:pointer + 4]
        memory[params[2]] = memory[params[0]] * memory[params[1]]
        return run_step(memory, pointer + 4)
    if instruction == 99:
        return memory

def run_program(memory, noun, verb):
    memory = list(memory)
    memory[1] = noun
    memory[2] = verb
    results = run_step(memory, pointer = 0)
    return results[0]

def find_inputs(target):
    for noun in range(100):
        for verb in range(100):
            if run_program(raw_input, noun, verb) == target:
                return (noun, verb)

raw_input = [int(address) for address in open('input.txt','r').read().split(',')]

print ('Answer 1:')
print (run_program(raw_input, 12, 2))

(noun, verb) = find_inputs(19690720)

print ('Answer 2:')
print (100 * noun + verb)
