import sys
import json
import numpy as np
import matplotlib.pyplot as plt

class Lines:
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.frames = []


class Frame:
    x = 0.0

    def __init__(self, *args, **kwargs):
        super().__init__()
        if len(args) > 0:
            self.yz = args[0][:]
        else:
            self.yz = []
        self.chines = []


def load_lines_plan(filename):
    result = Lines()
    with open(filename) as f:
        data = json.loads(f.read())
        for f in data:
            frame = Frame()
            f.x = f['x']
            f.yz = f['yz']
            f.chines = f['chines']
            result.frames.append(frame)
            

def plot_lines_plan(lines_plan):    
    plt.clf()
    for frame in lines_plan.frames:
        a = np.asarray(frame.yz)
        plt.plot(a.T[0,:], a.T[1,:])    
    plt.axis('equal')
    plt.show()
