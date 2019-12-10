import math
from itertools import cycle


def gcf(x, y):
    while (y):
        x, y = y, x % y
    return x


def v_to_dir(v):
    (x, y) = v
    f = abs(gcf(x, y))
    return (x // f, y // f)


def sort_by_dist(vectors):
    return [v for d, v in sorted([(abs(v[0]) + abs(v[1]), v) for v in vectors])]


def dir_to_angle(dir):
    return math.atan2(dir[0], dir[1]) / math.pi * -180 + 180


def sort_by_angle(sightlines):
    return [asteroids for angle, asteroids in
            sorted([(dir_to_angle(dir), asteroids) for (dir, asteroids) in sightlines])]


asteroids = [(x, y) for y, row in enumerate(open('input.txt', 'r').read().split('\n')) for x, cell in
             enumerate(list(row)) if cell == '#']

visibility = {}
# each asteroid is a key, each value is a dict of directions
# each key in a directions dict is a (x,y) direction containing one of more asteroids
# the values in a directions dict are the asteroids in that directions, is ascending distance order
# eg. (1,2): [(1,2), (2,4), (4,8)]

for a in asteroids:
    dirs = {}
    for b in asteroids:
        if a != b:
            v = (b[0] - a[0], b[1] - a[1])
            dir = v_to_dir(v)
            if dir not in dirs:
                dirs[dir] = []
            dirs[dir].append(v)
    for dir in dirs:
        dirs[dir] = sort_by_dist(dirs[dir])
    visibility[a] = dirs

(max_visibility, land_at) = max([(len(dirs), asteroid) for (asteroid, dirs) in visibility.items()])

print('Answer 1:')
print(max_visibility)

sightlines = sort_by_angle(visibility[land_at].items())
sightline_cycle = cycle(sightlines)

destroyed_count = 0
while any([len(s) > 0 for s in sightlines]):
    targeted = next(sightline_cycle)
    if len(targeted) > 0:
        destroyed = targeted.pop(0)
        destroyed_count += 1
        if destroyed_count == 200:
            winner = (destroyed[0] + land_at[0], destroyed[1] + land_at[1])

print('Answer 2:')
print(winner[0] * 100 + winner[1])
