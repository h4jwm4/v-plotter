import matplotlib.pyplot as plt
import numpy as np
# Parameters
n = 100  # number of points on each axis
size = 10  # canvas size

# Generate points along the left and bottom edges
x_points = np.linspace(0, size, n)
y_points = np.linspace(0, size, n)

# Create figure
plt.figure(figsize=(6, 6))
plt.axis('equal')
plt.axis('off')

# Start with first point
x = []
y = []

# Draw lines from left to bottom (single continuous path)
for i in range(n):
    x.append(0)
    y.append(y_points[i])
    x.append(x_points[i])
    y.append(0)

# Plot as one continuous line
plt.plot(x, y, color='black', linewidth=1)
plt.title("Continuous String Art with Straight Lines", fontsize=14)
plt.show()
