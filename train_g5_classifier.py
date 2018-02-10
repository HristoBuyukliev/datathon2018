import numpy as np
from data import read_g5
from keras.layers import *
from keras.models import Model
from keras.optimizers import Adam
from sklearn.metrics import confusion_matrix
from keras.callbacks import Callback
id2word = [x.strip() for x in open('vocab.txt')]
w2id = {w:i for i,w in enumerate(id2word)}
embeddings = np.loadtxt('wv.vec')
g5 = read_g5()

g5_indices = [w2id[x] for x in g5['HASH_ID'] if x in w2id]
ys = np.zeros(embeddings.shape[0])
ys[g5_indices] = 1
print(np.sum(ys))


class Evaluator(Callback):

    def on_epoch_end(self, epoch, logs=None):
        evaluate(self.model)

def evaluate(m):
    predictions = m.predict(embeddings)
    predictions = predictions.round()
    print(confusion_matrix(ys, predictions))


def get_model():
    input = Input((64,))
    out = Dense(1, activation='sigmoid')(input)
    model = Model(input, out)
    model.compile(Adam(), 'binary_crossentropy', metrics=["accuracy"])
    return model

m = get_model()
m.fit(embeddings,ys, validation_split=0.05, epochs=10, class_weight=[1,10000], callbacks=[Evaluator()])
predictions = m.predict(embeddings)
predictions = predictions.round()
print(confusion_matrix(ys, predictions))