import collections
import operator
from time import time
import pandas as pd


def main(fp):
    start = time()
    seen = set()
    outnodes = collections.defaultdict(lambda: [])
    innodes = collections.defaultdict(lambda: [])
    usernames ={}
    with open(fp) as lines:
        for line in lines:
            stuff = line.split("\t")
            user_from = stuff[0]
            user_name = stuff[1].strip()
            usernames[user_from] = user_name
            users_to = set()
            if len(stuff)>3:
                users_to = set([x.strip() for x in stuff[3].split(",") if x.strip() !=''])
            outnodes[user_from] = users_to
            seen.add(user_from)
            for user in users_to:
                seen.add(user)
                innodes[user].append(user_from)
    oldhubs = collections.defaultdict(lambda: (len(seen) ** -0.5))
    oldauthorities = collections.defaultdict(lambda: (len(seen) ** -0.5))

    for i in range(150):
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

    auth = sorted(oldauthorities.items(), key=operator.itemgetter(1))
    hubs = sorted(oldhubs.items(), key=operator.itemgetter(1))

    with open('%s.hubs.txt' % fp, 'w') as out:
        for u_id, score in hubs:
            out.write("\t".join([str(round(score, 8)),
                                 str(oldauthorities[u_id]),
                                 str(u_id),
                                 usernames[u_id.strip()] if u_id.strip() in usernames else 'unknown',
                                 'Responded to %i users' % len(outnodes[u_id]),
                                 'Got responses from %i users' % len(innodes[u_id])]) + "\n")

    with open('%s.auth.txt' % fp, 'w') as out:
        for u_id, score in auth:
            out.write("\t".join([str(round(score, 8)),
                                 str(oldhubs[u_id]),
                                 str(u_id),
                                 usernames[u_id.strip()] if u_id.strip() in usernames else 'unknown',
                                 'Responded to %i users' % len(outnodes[u_id]),
                                 'Got responses from %i users' % len(innodes[u_id])]) + "\n")
    print(fp + " Complete")
    return time() - start


def read_data():
    return pd.read_csv('')