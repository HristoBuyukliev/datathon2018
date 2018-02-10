import collections
import operator
from time import time
from link import Link
from data import read_data



def normalize(values:dict):
    normalization_value = sum(x**2 for x in values.values()) ** 0.5
    return {key: value/ normalization_value for (key,value) in values.items()}

def main(data, fp, use_weights =False):
    start = time()
    seen = set()
    outnodes = collections.defaultdict(lambda: set())
    innodes = collections.defaultdict(lambda: set()) # only use for the stats at the end. Do not use it in the algorithm
    for i, r in data.iterrows():
        user_from = i[0]
        user_to = i[1]
        l = Link(user_from, user_to, r['strength'])
        outnodes[user_from].add(l)
        innodes[user_to].add(user_from)
        seen.add(user_from)
        seen.add(user_to)
    print("Graph created")
    oldhubs = collections.defaultdict(lambda: (len(seen) ** -0.5))
    oldauthorities = collections.defaultdict(lambda: (len(seen) ** -0.5))

    for i in range(100):
        newhubs = collections.defaultdict(lambda: 0)
        newauthorities = collections.defaultdict(lambda: 0)
        for vertex in seen:
            for link in outnodes[vertex]:
                if use_weights:
                    newhubs[vertex] += oldauthorities[link.target] * min(link.strength, 1)
                    newauthorities[link.target] += oldhubs[vertex] * min(link.strength, 1)
                else:
                    newhubs[vertex] += oldauthorities[link.target]
                    newauthorities[link.target] += oldhubs[vertex]
        newhubs = normalize(newhubs)
        newauthorities = normalize(newauthorities)
        delta = sum([abs(newhubs[t] - oldhubs[t]) for t in newhubs])
        print("Delta", delta)
        oldhubs = newhubs
        oldauthorities = newauthorities

    auth = sorted(oldauthorities.items(), key=operator.itemgetter(1), reverse=True)
    hubs = sorted(oldhubs.items(), key=operator.itemgetter(1), reverse=True)

    with open('%s.hubs.txt' % fp, 'w') as out:
        for u_id, score in hubs:
            out.write("\t".join([str(round(score, 8)),
                                 str(oldauthorities.get(u_id, 0)),
                                 str(u_id),
                                 'Out degree  %i ' % len(outnodes[u_id]),
                                 'In degree %i users' % len(innodes[u_id])]) + "\n")

    with open('%s.auth.txt' % fp, 'w') as out:
        for u_id, score in auth:
            out.write("\t".join([str(round(score, 8)),
                                 str(oldhubs.get(u_id,0)),
                                 str(u_id),
                                 'Responded to %i users' % len(outnodes[u_id]),
                                 'Got responses from %i users' % len(innodes[u_id])]) + "\n")
    print(fp + " Complete")
    return time() - start


graphData = read_data()

main(graphData, '404-weighted', True)