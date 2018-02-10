from gensim.models import Word2Vec
from data import read_data
import numpy as np

def dist(x, y):
    return np.sqrt(np.sum(np.square(x-y),axis=1))


id2word = [x.strip() for x in open('vocab.txt')]
w2id = {w:i for i,w in enumerate(id2word)}
graphData = read_data()

embeddings = np.loadtxt('wv.vec')

count_failed = 0
batch_correct_1 = []
batch_correct_2 = []
batch_random_1 = []
batch_random_2 = []
for i, (key, r) in enumerate(graphData.iterrows()):
    if (i+1) % 1000 == 0:
        print(i)
    from_node = key[0]
    to_node = key[1]
    random_node = np.random.choice(len(id2word))
    wv1 = embeddings[w2id[from_node]]
    wv2 = embeddings[w2id[to_node]]
    wvr = embeddings[random_node]

    batch_correct_1.append(wv1)
    batch_correct_2.append(wv2)

    batch_random_1.append(wv1)
    batch_random_2.append(wvr)

distances_l = dist(np.array(batch_correct_1), np.array(batch_correct_2))
distances_r = dist(np.array(batch_random_1), np.array(batch_random_2))
print("Correct", np.sum(distances_l < distances_r))
print("Mean Distance linked", np.mean(distances_l))
print("Std Distance linked", np.std(distances_l))
print("Mean Distance random", np.mean(distances_r))
print("Std Distance random", np.std(distances_r))
