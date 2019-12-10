import re
import networkx as nx

orbits = nx.Graph()
orbits.add_node('COM')

for l in open('input.txt','r').readlines():
    regex = '(.*)\)(.*)'
    (orbited, orbiting) = re.findall(regex, l)[0]
    orbits.add_node(orbited)
    orbits.add_node(orbiting)
    orbits.add_edge(orbited, orbiting)

print ('Answer 1:')
print(sum([len(nx.shortest_path(orbits, 'COM', node)) - 1 for node in orbits.nodes]))

print ('Answer 2:')
print (len(nx.shortest_path(orbits, 'YOU', 'SAN')) - 1 - 2)
