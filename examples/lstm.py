import numpy as np

from deepx.nn import *
from deepx.rnn import *
from deepx.loss import *
from deepx.optimize import *

if __name__ == "__main__":
    lstm = Sequence(Image((1, 28, 28), 10), 10) >> Conv((10, 2, 2)) >> Conv((20, 2, 2)) >> Flatten() >> LSTM(100)
    model = Last(lstm) >> Softmax(10)

    rmsprop = RMSProp(model, CrossEntropy())
