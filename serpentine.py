import matplotlib.pyplot as plt

# Initialize lists to store coordinates
x_coords = []
y_coords = []

# Start from y = 0, increment by 10 until y = 100
y = 0
direction = 1  # 1 = left to right, -1 = right to left

while y <= 100:
    if direction == 1:
        x_range = range(0, 101)  # Left to right
    else:
        x_range = range(100, -1, -1)  # Right to left

    for x in x_range:
        x_coords.append(x)
        y_coords.append(y)

    y += 10
    direction *= -1  # Flip direction

# Plot the path
plt.figure(figsize=(10, 6))
plt.plot(x_coords, y_coords, color='blue')
plt.title("Zig-Zag Pattern")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.axis("equal")
plt.show()
