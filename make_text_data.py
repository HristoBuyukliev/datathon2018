import collections
from data import read_data
from random import shuffle


graphData = read_data()
neighbours = collections.defaultdict(lambda: set())
for i, r in graphData.iterrows():
    user_from = i[0]
    user_to = i[1]
    neighbours[user_from].add(user_to)
    neighbours[user_to].add(user_from)



with open('graph-as-text.txt','w') as out:
    for node, node_neighbours in neighbours.items():
        l = [node] + list(node_neighbours)
        if len(l) > 1:
            for _ in range(len(l)):
                shuffle(l)
                out.write(" ".join(l)+'\n')