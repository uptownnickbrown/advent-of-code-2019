def has_double(num):
    return any([str(d) * 2 in str(num) for d in range(0,10)])

def is_increasing(num):
    return all([int(d) >= int(str(num)[i-1]) for i, d in enumerate(str(num)) if i > 0])

def has_exact_double(num):
    return any([True for i, d in enumerate(range(0,10)) if str(d) * 2 in str(num) and str(d) * 3 not in str(num)])

min_in = 136760
max_in = 595730

print ('Answer 1:')
print (sum([has_double(i) and is_increasing(i) for i in range(min_in, max_in + 1)]))

print ('Answer 2:')
print (sum([has_exact_double(i) and is_increasing(i) for i in range(min_in, max_in + 1)]))