import collections
import operator
from time import time

from data import read_data


def main(data, fp):
    start = time()
    seen = set()
    outnodes = collections.defaultdict(lambda: set())
    innodes = collections.defaultdict(lambda: set())
    for i, r in data.iterrows():
        user_from = i[0]
        user_to = i[1]
        outnodes[user_from].add(user_to)
        innodes[user_to].add(user_from)
        seen.add(user_from)
        seen.add(user_to)
    print("Graph created")
    oldhubs = collections.defaultdict(lambda: (len(seen) ** -0.5))
    oldauthorities = collections.defaultdict(lambda: (len(seen) ** -0.5))

    for i in range(100):
        sumhubs = 0
        sumauth = 0
        newhubs = collections.defaultdict(lambda: 0)
        newauthorities = collections.defaultdict(lambda: 0)
        for vertex in seen:
            for auth in outnodes[vertex]:
                newhubs[vertex] += oldauthorities[auth]
            sumhubs += newhubs[vertex] ** 2
        for vertex in seen:
            for hub in innodes[vertex]:
                newauthorities[vertex] += oldhubs[hub]
            sumauth += newauthorities[vertex] ** 2
        sumhubs = sumhubs ** 0.5
        sumauth = sumauth ** 0.5
        newhubs = {t: newhubs[t] / sumhubs for t in newhubs}
        newauthorities = {t: newauthorities[t] / sumauth for t in newauthorities}
        delta = sum([abs(newhubs[t] - oldhubs[t]) for t in newhubs])
        print("Delta", delta)
        oldhubs = newhubs
        oldauthorities = newauthorities

    auth = sorted(oldauthorities.items(), key=operator.itemgetter(1), reverse=True)
    hubs = sorted(oldhubs.items(), key=operator.itemgetter(1), reverse=True)

    with open('%s.hubs.txt' % fp, 'w') as out:
        for u_id, score in hubs:
            out.write("\t".join([str(round(score, 8)),
                                 str(oldauthorities[u_id]),
                                 str(u_id),
                                 'Out degree  %i ' % len(outnodes[u_id]),
                                 'In degree %i users' % len(innodes[u_id])]) + "\n")

    with open('%s.auth.txt' % fp, 'w') as out:
        for u_id, score in auth:
            out.write("\t".join([str(round(score, 8)),
                                 str(oldhubs[u_id]),
                                 str(u_id),
                                 'Responded to %i users' % len(outnodes[u_id]),
                                 'Got responses from %i users' % len(innodes[u_id])]) + "\n")
    print(fp + " Complete")
    return time() - start


graphData = read_data()

main(graphData, '404')