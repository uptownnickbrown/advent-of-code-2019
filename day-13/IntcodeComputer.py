from defaultlist import defaultlist


class Operation:
    def __init__(self, entry):
        self.instruction = entry % 100
        self.modes = [int(mode) for mode in reversed(str(entry // 100))]
        op_param_map = {
            1: 3,
            2: 3,
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            9: 1,
            99: 0
        }
        self.param_count = op_param_map[self.instruction]
        self.modes.extend([0] * (self.param_count - len(self.modes)))


class ParameterSet:
    def __init__(self, computer, operation):
        self.modes = operation.modes
        self.params = [Parameter(computer, entry, self.modes[i]) for i, entry in
                       enumerate(computer.memory[computer.pointer + 1:computer.pointer + 1 + operation.param_count])]

    def __iter__(self):
        for param in self.params:
            yield param

    def __getitem__(self, sub):
        return self.params[sub]


class Parameter:
    def __init__(self, computer, entry, mode):
        self.entry = entry
        self.mode = mode
        if self.mode == 0:
            self.val = computer.memory[self.entry]
        elif self.mode == 1:
            self.val = self.entry
        elif self.mode == 2:
            self.val = computer.memory[computer.relative_base + self.entry]
        else:
            raise Exception('Unexpected parameter mode!')


class Computer:
    def __init__(self, memory):
        self.memory = defaultlist(lambda: 0)
        for i, entry in enumerate(memory):
            self.memory[i] = entry
        self.pointer = 0
        self.relative_base = 0

        self.inputs = None
        self.outputs = []
        self.complete = False

    def write(self, param, val):
        if param.mode == 2:
            self.memory[param.entry + self.relative_base] = val
        else:
            self.memory[param.entry] = val

    def incr_pointer(self, op):
        self.pointer = self.pointer + op.param_count + 1

    def run_step(self):
        op = Operation(self.memory[self.pointer])
        if op.instruction == 1:
            (op_1, op_2, out) = ParameterSet(self, op)
            self.write(out, op_1.val + op_2.val)
            self.incr_pointer(op)
        elif op.instruction == 2:
            (op_1, op_2, out) = ParameterSet(self, op)
            self.write(out, op_1.val * op_2.val)
            self.incr_pointer(op)
        elif op.instruction == 3:
            if len(self.inputs) == 0:
                # causes run_to_pause to pause and wait for next input
                return True
            (out,) = ParameterSet(self, op)
            self.write(out, self.inputs.pop(0))
            self.incr_pointer(op)
        elif op.instruction == 4:
            (loc,) = ParameterSet(self, op)
            self.outputs.append(loc.val)
            self.incr_pointer(op)
        elif op.instruction == 5:
            (check, jump) = ParameterSet(self, op)
            if check.val != 0:
                self.pointer = jump.val
            else:
                self.incr_pointer(op)
        elif op.instruction == 6:
            (check, jump) = ParameterSet(self, op)
            if check.val == 0:
                self.pointer = jump.val
            else:
                self.incr_pointer(op)
        elif op.instruction == 7:
            (check_1, check_2, out) = ParameterSet(self, op)
            if check_1.val < check_2.val:
                self.write(out, 1)
            else:
                self.write(out, 0)
            self.incr_pointer(op)
        elif op.instruction == 8:
            (check_1, check_2, out) = ParameterSet(self, op)
            if check_1.val == check_2.val:
                self.write(out, 1)
            else:
                self.write(out, 0)
            self.incr_pointer(op)
        elif op.instruction == 9:
            (base_offset,) = ParameterSet(self, op)
            self.relative_base += base_offset.val
            self.incr_pointer(op)
        elif op.instruction == 99:
            self.complete = True
            return True
        else:
            raise Exception('Unexpected instruction!')
        return False

    def run_to_pause(self, inputs=[]):
        self.inputs = inputs
        while self.complete == False:
            if self.run_step() == True:
                break

    def run_program(self, noun=None, verb=None, inputs=[]):
        self.inputs = inputs
        self.pointer = 0
        self.outputs = []
        if noun:
            self.memory[1] = noun
        if verb:
            self.memory[2] = verb
        while self.complete == False:
            if self.run_step() == True:
                break
        return self.outputs
