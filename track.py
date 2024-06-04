import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import json 

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
        self.path = [np.array(initial_loc) + np.array([i, i**2, i**3]) for i in range(15)]

# Create the radars and intruder
radars = {
    'A': Radar('A', [1, 1, 1], [1, 0, 0], 15),
    'B': Radar('B', [5, 5, 2], [0, 1, 0], 19),
    'C': Radar('C', [4, 10, 10], [0, 0, 1], 20),
    'D': Radar('D', [10, 8, 3], [0, 1, 1], 40)
}
intruder = Intruder([1, 1, 10])

intruder_x = [loc[0] for loc in intruder.path]
intruder_y = [loc[1] for loc in intruder.path]
intruder_z = [loc[2] for loc in intruder.path]

# Fit polynomial models for x, y, z coordinates
degree = 3  # Degree of the polynomial
poly_x = np.polyfit(range(len(intruder_x)), intruder_x, degree)
poly_y = np.polyfit(range(len(intruder_y)), intruder_y, degree)
poly_z = np.polyfit(range(len(intruder_z)), intruder_z, degree)

# Generate predicted path
predicted_steps = range(len(intruder.path))
predicted_x = np.polyval(poly_x, predicted_steps)
predicted_y = np.polyval(poly_y, predicted_steps)
predicted_z = np.polyval(poly_z, predicted_steps)
predicted_path = [np.array([x, y, z]) for x, y, z in zip(predicted_x, predicted_y, predicted_z)]

# Plot the results
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for name, radar in radars.items():
    ax.scatter(*radar.loc, label=name)

output = []
red_points_count = 0  # Counter to keep track of the number of red points

for i, intruder_loc in enumerate(intruder.path):
    ax.scatter(*intruder_loc, color='pink')
    plt.pause(0.2)  # Pause for half a second
    detection = {}
    for name, radar in radars.items():
        if radar.detect_intruder(intruder_loc):
            detection[name] = list(intruder_loc.tolist())
            ax.scatter(*intruder_loc,color = 'red')
            plt.pause(0.2)  # Pause for half a second
            red_points_count += 1  # Increment the counter when a red point is plotted
    output.append(detection)

    # Start plotting the predicted path after 3 red points have been plotted
    if red_points_count >= 3:
        for pred_loc in predicted_path[i:]:
            ax.scatter(*pred_loc, color='blue')

with open('radar_data.json', 'w') as f:
    json.dump(output, f)



ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.legend()
plt.show()