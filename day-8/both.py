from collections import defaultdict

def chunkify_string(s, size):
    return [s[i:i+size] for i, val in enumerate(s) if i % size == 0]

def count_char(s, char):
    return len(s.split(char)) - 1

width = 25
height = 6

layers = chunkify_string(str(open('input.txt','r').read()), width * height)

min_zeros = 9999
min_zero_layer = None
for layer in layers:
    zeros = count_char(layer, '0')
    if zeros < min_zeros:
        min_zeros = zeros
        min_zero_layer = count_char(layer, '1') * count_char(layer, '2')
    rows = chunkify_string(layer, width)

print ('Answer 1:')
print (min_zero_layer)

composite = defaultdict(lambda: '2')
for layer in layers:
    rows = chunkify_string(layer, width)
    for row_ix, row in enumerate(rows):
        for col_ix, val in enumerate(row):
            if composite[(col_ix, row_ix)] == '2' and val != '2':
                if val == '1':
                    composite[(col_ix, row_ix)] = '@'
                if val == '0':
                    composite[(col_ix, row_ix)] = ' '

composite_rows = []

for y in range(height):
    composite_rows.append(''.join([composite[(x,y)] for x in range(width)]))

print ('Answer 2:')
print('\n'.join(composite_rows))
