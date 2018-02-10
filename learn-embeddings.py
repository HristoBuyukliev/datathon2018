from gensim.models import Word2Vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = [l.strip().split() for l in open('graph-as-text.txt')]
model = Word2Vec(sentences, sg=1, size=64, window=5, min_count=1, workers=4)
model.save('w2v.vec')


