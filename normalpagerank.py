import collections
import operator
from data import read_data
from pandas import DataFrame


def main(graphData: DataFrame, alpha=0.8):
    seen = set()
    outnodes = collections.defaultdict(lambda: set())
    innodes = collections.defaultdict(lambda: set())
    for i, r in graphData.iterrows():
        user_from = r['Subscriber_A']
        user_to = r['Subsciber_B']
        outnodes[user_from].add(user_to)
        innodes[user_to].add(user_from)
        seen.add(user_from)
        seen.add(user_to)
    print("Graph created")
    currentpageranks = collections.defaultdict(lambda: 1.0 / len(seen))
    newpageranks = collections.defaultdict()
    for iteration in range(100):
        C = 0
        print('seen', len(seen))
        print('senders', len(outnodes.keys()))
        print('sinks', len(seen - set(outnodes.keys())))
        for a in (seen - set(outnodes.keys())):
            C += currentpageranks[a]

        print(C)
        for r in seen:
            newpageranks[r] = (1 - alpha + alpha * C) / len(seen)
        for r in outnodes:
            q = outnodes[r]
            for entry in q:
                newpageranks[entry] += alpha * currentpageranks[r] / len(q)
        delta = sum(abs(currentpageranks[x]- newpageranks[x]) for x in newpageranks)
        print("Delta", delta)
        currentpageranks = newpageranks
        newpageranks = collections.defaultdict()
    return currentpageranks


graphData = read_data()
results = main(graphData)
pageranks = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

with open('pr.txt', 'w') as out:
    for pagerank in pageranks:
        out.write(str(round(pagerank[1], 8)) + " " + str(pagerank[0]))
        out.write('\n')
