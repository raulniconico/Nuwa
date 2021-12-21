import argparse

import numpy as np

import utils
from dataloader import Dataset
from network import NN
from optimizers import Optimizer
from visualization import Visual

if __name__ == "__main__":
    # parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path(s)')

    # total observation number
    n = 200
    # x1, x2 are generated by two
    x1 = np.random.uniform(0, 1, n)
    x2 = np.random.uniform(0, 1, n)
    const = np.ones(n)
    eps = np.random.normal(0, .05, n)
    b = 1.5
    theta1 = 2
    theta2 = 5
    Theta = np.array([b, theta1, theta2])
    y = np.array(b * const + theta1 * x1 + theta2 * x2 + eps)
    y = np.reshape(y, (-1, 1))
    X = np.array([const, x1, x2]).T

    layer_list = [NN.Layer('Linear',3,10,'sigmoid',BN=True), NN.Layer('Linear',10,100,'sigmoid',BN=True),
                  NN.Layer('Linear',100,10,'sigmoid',BN=True),NN.Layer('Linear',10,3,'none') ]
    dataset = Dataset(X, y, mini_batch= 64)
    nn = NN(dataset)
    nn.addlayers(layer_list)
    optim = Optimizer(nn,"minibatchgd",epoch = 1000, lr=1e-4, decay_rate=0.01)
    optim.train()
    visual = Visual(optim)
    visual.plotloss()
    visual.plotgradientnorm()

    layer_list = [NN.Layer('Linear',3,100,'LeakyReLU'),NN.Layer('Linear',100,3,'LeakyReLU'),
                  NN.Layer('Linear',3,1,'none')]
    dataset = Dataset(X, y)
    nn = NN(dataset)
    nn.addlayers(layer_list)
    optim = Optimizer(nn,"SGD",epoch = 10000, lr=1e-6)
    optim.train()
    visual = Visual(optim)
    visual.plotloss()
    visual.plotgradientnorm()