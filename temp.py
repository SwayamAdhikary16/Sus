import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import requests
import json

# Get elevation data
def get_elevation_open_elevation(lat, lon):
    url = 'https://api.open-elevation.com/api/v1/lookup'
    params = {'locations': f"{lat},{lon}"}
    response = requests.get(url, params=params)
    return response.json()['results'][0]['elevation']

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

# Your coordinates
center_lat = 17.809974606837404
center_lon = 83.2421106444674

# Define the size of the area (in degrees)
size = 0.1  # This is roughly equal to 1 km

# Create a grid of coordinates around the center point
lats = np.linspace(center_lat - size/2, center_lat + size/2, 10)
lons = np.linspace(center_lon - size/2, center_lon + size/2, 10)

# Initialize an array to hold the elevations
elevations = np.zeros((len(lats), len(lons)))

# Get the elevation for each coordinate
for i, lat in enumerate(lats):
    for j, lon in enumerate(lons):
        elevations[i, j] = get_elevation_open_elevation(lat, lon)

elevation = elevations - elevations.min()

# Create a colormap
norm = plt.Normalize(elevation.min(), elevation.max())
colors = cm.viridis(norm(elevation))

# Create the 3D bar plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y = np.meshgrid(lats, lons)
ax.bar3d(x.flatten(), y.flatten(), np.zeros(len(elevation.flatten())), 1/len(lats), 1/len(lons), elevation.flatten(), color=colors.reshape(-1,4), shade=True)

# Define a function to map the coordinates
def map_coordinates(coord, min_val, max_val):
    return (max_val - min_val) * (coord - 1) / 9 + min_val

# Function to generate radars
# Function to generate radars
def generate_radars(num_radars, radar_range, lats, lons, elevations):
    radars = {}
    for i in range(num_radars):
        # Generate random latitude and longitude indices
        lat_idx = np.random.randint(0, len(lats))
        lon_idx = np.random.randint(0, len(lons))

        # Get the corresponding latitude, longitude, and elevation
        lat = lats[lat_idx]
        lon = lons[lon_idx]
        elev = elevations[lat_idx, lon_idx] + 10

        # Generate a random direction
        dir = np.random.uniform(-1, 1, 3)  # 3D direction
        dir = dir / np.linalg.norm(dir)  # Normalize the direction vector

        # Add the radar to the dictionary
        radars[f'Radar{i+1}'] = Radar(f'Radar{i+1}', [lat, lon, elev], dir, radar_range)
    return radars


# Create the radars and intruder
radars = generate_radars(4, 15, lats, lons, elevations)
intruder = Intruder([map_coordinates(1, center_lat - size/2, center_lat + size/2), map_coordinates(1, center_lon - size/2, center_lon + size/2), 10])

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

for name, radar in radars.items():
    ax.scatter(*radar.loc, label=name)

output = []
red_points_count = 0  # Counter to keep track of the number of red points

# for i, intruder_loc in enumerate(intruder.path):
#     ax.scatter(*intruder_loc, color='pink')
#     plt.pause(0.2)  # Pause for half a second
#     detection = {}
#     for name, radar in radars.items():
#         if radar.detect_intruder(intruder_loc):
#             detection[name] = intruder_loc
#             ax.scatter(*intruder_loc,color = 'red')
#             plt.pause(0.2)  # Pause for half a second
#             red_points_count += 1  # Increment the counter when a red point is plotted
#     output.append(detection)

    # Start plotting the predicted path after 3 red points have been plotted
    # if red_points_count >= 3:
    #     for pred_loc in predicted_path[i:]:
    #         ax.scatter(*pred_loc, color='blue')

# Convert numpy.int32 to int before writing to JSON


for i in range(len(output)):
    for name in output[i]:
        output[i][name] = [int(x) for x in output[i][name]]

with open('radar_data.json', 'w') as f:
    json.dump(output, f)

ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Elevation')

plt.legend()
plt.show()
