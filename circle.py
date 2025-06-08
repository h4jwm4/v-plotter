import numpy as np
import matplotlib.pyplot as plt

# Circle parameters
x_center = 0.5
y_center = 0.5
radius = 0.3

# Generate theta values from 0 to 2π
theta = np.linspace(0, 2 * np.pi, 100)

# Compute x and y coordinates
x = x_center + radius * np.cos(theta)
y = y_center + radius * np.sin(theta)

# Store coordinates in a list of tuples (optional)
circle_coords = list(zip(x, y))

# Print first 5 coordinates
print(circle_coords[:5])

# Plot the circle
plt.plot(x, y)
plt.gca().set_aspect('equal')
plt.title("Circle using (x, y) coordinates")
plt.grid(True)
plt.show()
