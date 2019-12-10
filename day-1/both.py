def get_fuel(mass):
    return int(mass) // 3 - 2

def get_total_fuel(mass):
    total_fuel = get_fuel(mass)
    added_fuel = get_fuel(total_fuel)
    while added_fuel > 0:
        total_fuel = total_fuel + added_fuel
        added_fuel = get_fuel(added_fuel)
    return total_fuel

print ('Answer 1:')
print (sum([get_fuel(l) for l in open('input.txt','r').readlines()]))

print ('Answer 2:')
print (sum([get_total_fuel(l) for l in open('input.txt','r').readlines()]))
