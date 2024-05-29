import matplotlib.pyplot as plt
import json
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class Radar:
    def __init__(self, name, loc, dir, range):
        self.name = name
        self.loc = loc
        self.dir = dir
        self.range = range

    def detect_intruder(self, intruder_loc):
        distance = np.sqrt((self.loc[0] - intruder_loc[0])**2 + (self.loc[1] - intruder_loc[1])**2 + (self.loc[2] - intruder_loc[2])**2)
        intruder_dir = np.array(intruder_loc) - np.array(self.loc)
        intruder_dir = intruder_dir / np.linalg.norm(intruder_dir)
        return distance <= self.range and np.dot(self.dir, intruder_dir) > 0

class Intruder:
    def __init__(self, initial_loc):
        self.path = [np.array(initial_loc) + np.array([i, i, abs(-i**2/11 + i)]) for i in range(15)]

radars = {
    'A': Radar('A', [1, 1, 1], [1, 0, 0], 10),
    'B': Radar('B', [5, 5, 2], [0, 1, 0], 8),
    'C': Radar('C', [4, 10, 10], [0, 0, 1], 6),
    'D': Radar('D', [10, 8, 3], [0, 1, 0], 7)
}

intruder = Intruder([1,1,10])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for name, radar in radars.items():
    ax.scatter(*radar.loc, label=name)

output = []
for intruder_loc in intruder.path:
    ax.scatter(*intruder_loc, color='yellow')
    plt.pause(0.2)  # Pause for half a second
    detection = {}
    for name, radar in radars.items():
        if radar.detect_intruder(intruder_loc):
            detection[name] = list(intruder_loc.tolist())
            ax.scatter(*intruder_loc,color = 'red')
            plt.pause(0.2)  # Pause for half a second
    output.append(detection)

with open('radar_data.json', 'w') as f:
    json.dump(output, f)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.legend()
plt.show()
