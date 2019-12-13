import re
from itertools import combinations
from math import gcd

moons = []
for l in open('input.txt','r').readlines():
    (x,y,z) = re.findall('\<x=([-]?\d+), y=([-]?\d+), z=([-]?\d+)>',l)[0]
    moons.append([[int(x),0],[int(y),0],[int(z),0]])

def step_dim(moons, dim):
    for a, b in combinations(range(4), 2):
        a = moons[a]
        b = moons[b]
        if a[dim][0] > b[dim][0]:
            a[dim][1] += -1
            b[dim][1] += 1
        elif a[dim][0] < b[dim][0]:
            a[dim][1] += 1
            b[dim][1] += -1
    for moon in moons:
        moon[dim][0] += moon[dim][1]

def step(moons):
    for dim in range(3):
        step_dim(moons, dim)

def dim_state(moons, dim):
    return tuple([tuple(moon[dim]) for moon in moons])

def find_loop(moons, dim):
    history = set()
    curr = dim_state(moons, dim)
    while curr not in history:
        history.add(curr)
        step_dim(moons, dim)
        curr = dim_state(moons, dim)
    return len(history)

def lcm(a, b):
    return a * b // gcd(a,b)

def multi_lcm(nums):
    assert len(nums) > 2
    curr_lcm = lcm(nums.pop(), nums.pop())
    while nums:
        curr_lcm = lcm(curr_lcm, nums.pop())
    return curr_lcm

print(multi_lcm([find_loop(moons, i) for i in range(3)]))