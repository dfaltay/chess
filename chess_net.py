"""
This file and its tests are individualized for NetID bkaracan.
"""
import numpy as np
import torch as tr
from torch.nn import Sequential, Conv2d, Linear, Flatten, LeakyReLU, Tanh, Module, functional
import chess_withMinimax_plusNN as game_file

class PrintLayer(Module):
    def __init__(self):
        super(PrintLayer, self).__init__()
    
    def forward(self, x):
        # Do your print / debug stuff here
        print(x.shape)
        return x

def ChessNet1(selection):

    state = game_file.initial_state(selection)

    module = Sequential(Flatten(), Linear(3*len(state.board)*len(state.board[0]), 1, True))
    return module


class ChessNet2(Module):

    def __init__(self, selection):
        super(ChessNet2, self).__init__()
        self.value = 5
        self.selection = int(selection)
        self.conv1 = Conv2d(3, 8, 3)
        self.conv2 = Conv2d(8, 16, 3)
        self.fc1 = Linear(16*4*(self.value-self.selection), 1)

    def forward(self, x):
        x = functional.relu(self.conv1(x))
        x = functional.relu(self.conv2(x))
        x = x.view(-1, 16*4*(self.value-self.selection))
        x = functional.relu(self.fc1(x))
        return x

# def ChessNet2(selection):
#     layers = []
#     layers.append(Conv2d(3, 16, 3))
#     layers.append(PrintLayer())
#     layers.append(LeakyReLU())
#     layers.append(Conv2d(16, 32, 2))
#     layers.append(PrintLayer())
#     layers.append(LeakyReLU())
#     layers.append(Linear(490*16*4, 1))
#     layers.append(PrintLayer())
#     # layers.append(Linear(4, 1))
#     # layers.append(PrintLayer())
#     module = Sequential(*layers)

#     return module


def calculate_loss(net, x, y_targ):
    
    y = net(x)
    e = tr.sum((y-y_targ)**2)
	
    return (y, e)

def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y, e = calculate_loss(net, x, y_targ)
    e.backward()
    optimizer.step()
    return (y, e)


if __name__ == "__main__":

    
    selection = '1'
    # net = ChessNet2(selection)
    net = ChessNet2(selection)
    print(net)

    import pickle as pk
    with open("data%d.pkl" %int(selection),"rb") as f: (x, y_targ) = pk.load(f)

    # Optimization loop
    optimizer = tr.optim.Adam(net.parameters())
    train_loss, test_loss = [], []
    shuffle = np.random.permutation(range(len(x)))
    split = 10
    train, test = shuffle[:-split], shuffle[-split:]
    for epoch in range(5000):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle)-split))
        test_loss.append(e_test.item() / split)
    
    tr.save(net.state_dict(), "model%d.pth" % int(selection))
    
    import matplotlib.pyplot as pt
    pt.plot(train_loss,'b-')
    pt.plot(test_loss,'r-')
    pt.legend(["Train","Test"])
    pt.xlabel("Iteration")
    pt.ylabel("Average Loss")
    pt.savefig('LossFig_for_size%d.png'%int(selection))
    pt.clf()

    pt.plot(y_train.detach().numpy(), y_targ[train].detach().numpy(),'bo')
    pt.plot(y_test.detach().numpy(), y_targ[test].detach().numpy(),'ro')
    pt.legend(["Train","Test"])
    pt.xlabel("Actual output")
    pt.ylabel("Target output")
    pt.savefig('ScatterFig_for_size%d.png'%int(selection))

    

