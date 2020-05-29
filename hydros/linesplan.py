import sys
import json
import numpy as np
import matplotlib.pyplot as plt


def load_lines_plan(filename):
    with open(filename) as f:
        return json.loads(f.read())


def plot_lines_plan(lines_plan):    
    plt.clf()
    for i, a in enumerate(lines_plan['frames']):
        a = np.asarray(a['yz'])
        plt.plot(a.T[0,:], a.T[1,:])    
    plt.axis('equal')
    plt.show()
