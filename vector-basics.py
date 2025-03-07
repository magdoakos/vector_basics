import numpy as np
from geopy.distance import geodesic

# Example GPS data: list of (longitude, latitude, timestamp) tuples
gps_data = [
    (lon1, lat1, t1),
    (lon2, lat2, t2),
    (lon3, lat3, t3),
    # ... more data
]

# Extract coordinates and timestamps
coordinates = np.array([(data[0], data[1]) for data in gps_data])  # (lon, lat)
timestamps = np.array([data[2] for data in gps_data])

# Calculate displacements using differences in coordinates
displacements = np.diff(coordinates, axis=0)

# Calculate time differences
time_diffs = np.diff(timestamps)

# Calculate speed using geodesic distances
speeds = []
for i in range(len(coordinates) - 1):
    point1 = coordinates[i][::-1]  # (lat, lon)
    point2 = coordinates[i+1][::-1]
    distance = geodesic(point1, point2).meters  # Distance in meters
    speed = distance / time_diffs[i]  # Speed in meters per second
    speeds.append(speed)

# Calculate bearings
def calculate_bearing(pointA, pointB):
    lon1, lat1 = map(radians, pointA)
    lon2, lat2 = map(radians, pointB)
    dlon = lon2 - lon1
    x = sin(dlon) * cos(lat2)
    y = cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(dlon)
    initial_bearing = atan2(x, y)
    initial_bearing = np.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

bearings = []
for i in range(len(coordinates) - 1):
    bearing = calculate_bearing(coordinates[i], coordinates[i+1])
    bearings.append(bearing)
