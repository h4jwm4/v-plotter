import matplotlib.pyplot as plt
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch

# Step 1: Define the letter and font
letter = "A"
font = FontProperties(family="DejaVu Sans", size=100)

# Step 2: Get the text path
text_path = TextPath((0, 0), letter, prop=font)

# Step 3: Extract the vertices (coordinates)
vertices = text_path.vertices
codes = text_path.codes  # This tells how the path is constructed (move, line, curve, etc.)

# Step 4: Plot the coordinates
fig, ax = plt.subplots()
ax.plot(vertices[:, 0], vertices[:, 1], 'o-', label='Letter Path')
ax.set_aspect('equal')
ax.set_title(f"Coordinates of Letter '{letter}'")
ax.invert_yaxis()  # Optional: matches how fonts are usually rendered (y goes down)

# Optional: show path as patch
patch = PathPatch(text_path, facecolor='lightblue', edgecolor='black', lw=1)
ax.add_patch(patch)

plt.legend()
plt.grid(True)
plt.show()
