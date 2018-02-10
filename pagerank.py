import collections
import operator
from data import read_data
from pandas import DataFrame
from link import Link

def getWeights(outnodes):
    weights = {}
    for k, links in outnodes.items():
        normalization = sum(l.strength for l in links)
        weights[k] = [l.strength/normalization for l in links]
    return weights

def main(graphData: DataFrame, alpha=0.8, use_weights=False):
    seen = set()
    outnodes = collections.defaultdict(lambda: [])
    for i, r in graphData.iterrows():
        user_from = i[0]
        user_to = i[1]
        link = Link(user_from, user_to, r['strength'])
        outnodes[user_from].append(link)
        seen.add(user_from)
        seen.add(user_to)
    print("Graph created")
    currentpageranks = collections.defaultdict(lambda: 1.0 / len(seen))
    newpageranks = collections.defaultdict()
    weights = getWeights(outnodes)
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
        for r, outgoing in outnodes.items():
            current_weights = weights[r]
            for i, link in enumerate(outgoing):
                weight = 1/ len(outgoing)
                if use_weights:
                    weight = current_weights[i]
                newpageranks[link.target] += alpha * currentpageranks[r] * weight
        delta = sum(abs(currentpageranks[x]- newpageranks[x]) for x in newpageranks)
        print("Delta", delta)
        currentpageranks = newpageranks
        newpageranks = collections.defaultdict()
    return currentpageranks


graphData = read_data()
results = main(graphData, use_weights=True)
pageranks = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

with open('pr-weighted.txt', 'w') as out:
    for pagerank in pageranks:
        out.write(str(round(pagerank[1], 8)) + " " + str(pagerank[0]))
        out.write('\n')
