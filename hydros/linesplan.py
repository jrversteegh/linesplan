import sys
import json
import numpy as np
import matplotlib.pyplot as plt

class Frame:
    x = 0.0

    def __init__(self, *args, **kwargs):
        super().__init__()
        if len(args) > 0:
            self.yz = args[0][:]
        else:
            self.yz = []
        self.chines = []


    def scale(self, factor):
        scaled = np.asarray(self.yz) * factor
        self.yz = [list(i) for i in scaled]


    def offset(self, vector):
        offset = np.asarray(self.yz) + np.asarray(vector)
        self.yz = [list(i) for i in offset]



class Lines:
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.frames = []
        self.name = ''


    def close_frames(self, margin=5E-3):
        for frame in self.frames:
            if frame.yz[0][0] < margin:
                frame.yz[0][0] = 0.0
            else:
                frame.chines.insert(0, 1)
                frame.yz.insert(0, [0.0, frame.yz[0][1]])

            if frame.yz[-1][0] < margin: 
                frame.yz[-1][0] = 0.0
            else:
                frame.chines.append(len(frame.yz) - 1)
                frame.yz.append([0.0, frame.yz[-1][1]])


    def scale(self, factor):
        for frame in self.frames:
            frame.scale(factor)


    def save(self, filename):
        save_lines_plan(self, filename)



def load_lines_plan(filename):
    result = Lines()
    with open(filename) as f:
        data = json.loads(f.read())
        result.name = data['name']
        for f in data['frames']:
            frame = Frame()
            frame.x = f['x']
            frame.yz = f['yz']
            frame.chines = f['chines']
            result.frames.append(frame)
    return result
            

def save_lines_plan(lines, filename):
    frames = [ { "x": fr.x, "yz": fr.yz, "chines": fr.chines } for fr in lines.frames ]
    s = json.dumps({ "name": lines.name, "frames": frames }, indent=2)
    with open(filename, "w") as f:
        f.write(s)


def plot_lines_plan(lines_plan, show_legend=False):    
    plt.clf()
    for i, frame in enumerate(lines_plan.frames):
        a = np.asarray(frame.yz)
        plt.plot(a.T[0,:], a.T[1,:], label=str(i))
    if show_legend:
        plt.legend()
    plt.axis('equal')
    plt.show()


def line_segments(line):
    line = np.asarray(line)
    segments = line[1:] - line[:-1]
    return [list(i) for i in segments]


def line_lengths(line):
    line = np.asarray(line)
    segments = line[1:] - line[:-1]
    segments *= segments
    lengths = np.sqrt(segments[:,0] + segments[:1])
    return list(lengths)
