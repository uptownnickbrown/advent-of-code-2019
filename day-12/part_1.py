import re
from itertools import combinations

# started 11:11

def compare_moons(a, b):
    if a.x > b.x:
        x = 1
    elif a.x == b.x:
        x = 0
    else:
        x = -1
    if a.y > b.y:
        y = 1
    elif a.y == b.y:
        y = 0
    else:
        y = -1
    if a.z > b.z:
        z = 1
    elif a.z == b.z:
        z = 0
    else:
        z = -1
    return (x,y,z)

class Moon:
    def __init__(self, position):
        # Example: <x=1, y=2, z=-9>
        regex = '\<x=([-]?\d+), y=([-]?\d+), z=([-]?\d+)>'
        (x,y,z) = re.findall(regex,position)[0]
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.x_v = 0
        self.y_v = 0
        self.z_v = 0

    def state_tuple(self):
        return (self.x, self.y, self.z, self.x_v, self.y_v, self.z_v)

    def energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.x_v) + abs(self.y_v) + abs(self.z_v))

    def __repr__(self):
        return f'Position: {self.x},{self.y},{self.z}. Velocity: {self.x_v},{self.y_v},{self.z_v}'

class OrbitalSystem:
    def __init__(self, moons):
        self.moons = moons
        self.timestep = 0
        self.states = set()
        self.states.add(tuple([moon.state_tuple() for moon in self.moons]))
        self.at_unity = False

    def step(self):
        for a, b in combinations(self.moons, 2):
            (x,y,z) = compare_moons(a,b)
            a.x_v += -x
            a.y_v += -y
            a.z_v += -z
            b.x_v += x
            b.y_v += y
            b.z_v += z
        for moon in self.moons:
            moon.x = moon.x + moon.x_v
            moon.y = moon.y + moon.y_v
            moon.z = moon.z + moon.z_v
        system_state = tuple([moon.state_tuple() for moon in self.moons])
        if system_state in self.states:
            self.at_unity = True
        else:
            self.states.add(system_state)
        self.timestep += 1

    def calc_energy(self):
        return sum([moon.energy() for moon in self.moons])

    def __repr__(self):
        return f'At time step {self.timestep}, moons are at {self.moons}.'

system = OrbitalSystem([Moon(l) for l in open('input.txt','r').readlines()])

for i in range(1000):
    system.step()

# Done 11:31
print ('Answer 1:')
print(system.calc_energy())

system = OrbitalSystem([Moon(l) for l in open('input.txt','r').readlines()])

#while system.at_unity == False:
#    system.step()

print ('Answer 2:')
#print(system.timestep)
