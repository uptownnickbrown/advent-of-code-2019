from defaultlist import defaultlist

def get_params(memory, pointer, param_count, opcode):
    param_modes = [int(mode) for mode in reversed(str(opcode // 100))]
    param_modes.extend([0] * (param_count - len(param_modes)))
    params = memory[pointer + 1:pointer + 1 + param_count]
    return list(zip(params, param_modes))

def get_param_value(memory, param):
    if param[1] == 0:
        return memory[param[0]]
    elif param[1] == 1:
        return param[0]
    else:
        raise Exception('Unexpected parameter mode!')

def run_step(memory, pointer=0, input=None, outputs=[]):
    opcode = memory[pointer]
    instruction = opcode % 100
    if instruction == 1:
        param_count = 3
        (op_1, op_2, out) = get_params(memory, pointer, 3, opcode)
        memory[out[0]] = get_param_value(memory, op_1) + get_param_value(memory, op_2)
        return run_step(memory, pointer = pointer + param_count + 1, outputs=outputs)
    if instruction == 2:
        param_count = 3
        (op_1, op_2, out) = get_params(memory, pointer, param_count, opcode)
        memory[out[0]] = get_param_value(memory, op_1) * get_param_value(memory, op_2)
        return run_step(memory, pointer = pointer + param_count + 1, outputs=outputs)
    if instruction == 3:
        param_count = 1
        (output_loc, ) = get_params(memory, pointer, param_count, opcode)
        memory[output_loc[0]] = input
        return run_step(memory, pointer = pointer + param_count + 1, outputs=outputs)
    if instruction == 4:
        param_count = 1
        (loc,) = get_params(memory, pointer, param_count, opcode)
        outputs.append(get_param_value(memory, loc))
        return run_step(memory, pointer = pointer + param_count + 1, outputs=outputs)
    if instruction == 5:
        param_count = 2
        (check,val) = get_params(memory, pointer, param_count, opcode)
        if get_param_value(memory, check) != 0:
            return run_step(memory, pointer = get_param_value(memory,val), outputs=outputs)
        return run_step(memory, pointer = pointer + param_count + 1, outputs=outputs)
    if instruction == 6:
        param_count = 2
        (check,val) = get_params(memory, pointer, param_count, opcode)
        if get_param_value(memory, check) == 0:
            return run_step(memory, pointer = get_param_value(memory,val), outputs=outputs)
        return run_step(memory, pointer = pointer + param_count + 1, outputs=outputs)
    if instruction == 7:
        param_count = 3
        (check_1,check_2,out) = get_params(memory, pointer, param_count, opcode)
        if get_param_value(memory, check_1) < get_param_value(memory, check_2):
            memory[out[0]] = 1
        else:
            memory[out[0]] = 0
        return run_step(memory, pointer = pointer + param_count + 1, outputs=outputs)
    if instruction == 8:
        param_count = 3
        (check_1,check_2,out) = get_params(memory, pointer, param_count, opcode)
        if get_param_value(memory, check_1) == get_param_value(memory, check_2):
            memory[out[0]] = 1
        else:
            memory[out[0]] = 0
        return run_step(memory, pointer = pointer + param_count + 1, outputs=outputs)
    if instruction == 99:
        return (memory, outputs)
    raise Exception('Unexpected instruction!')

def run_program(memory, noun=None, verb=None, input=None):
    memory = list(memory)
    if noun:
        memory[1] = noun
    if verb:
        memory[2] = verb
    (memory, outputs) = run_step(memory, pointer = 0, input = input, outputs=[])
    assert all([output == 0 for output in outputs[:-1]])
    return outputs[-1]

raw_input = [int(address) for address in open('input.txt','r').read().split(',')]


print ('Answer 1:')
print (run_program(raw_input, input=1))

print ('Answer 1:')
print (run_program(raw_input, input=5))
