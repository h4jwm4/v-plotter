import math
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from svgpathtools import svg2paths2

# V-Plotter constants
MOTOR_DISTANCE = 779.0  # mm
STEP_SIZE = 0.04        # mm per step

# Convert (x, y) to motor steps
def coords_to_steps(x, y):
    left_length = math.hypot(x, y)
    right_length = math.hypot(MOTOR_DISTANCE - x, y)
    left_steps = int(left_length / STEP_SIZE)
    right_steps = int(right_length / STEP_SIZE)
    return left_steps, right_steps

def pen_lift(lift=True):
    if lift:
        for angle in range(130, 64, -1):
            ser.write(f"S:{angle}\n".encode())
            time.sleep(0.02)
    else:
        for angle in range(64, 131, 1):
            ser.write(f"S:{angle}\n".encode())
            time.sleep(0.02)

# Group points by path
def sample_svg_path(svg_file, spacing_mm=0.5, scale=1.0, offset_x=0, offset_y=0):
    paths, attributes, svg_attributes = svg2paths2(svg_file)
    grouped_paths = []

    for path in paths:
        path_points = []
        for segment in path:
            scaled_length = segment.length() * scale
            num_samples = max(1, int(scaled_length / spacing_mm))
            for i in range(num_samples + 1):
                t = i / num_samples
                point = segment.point(t)
                x = (point.real * scale) + offset_x
                y = (point.imag * scale) + offset_y
                path_points.append((x, y))
        if path_points:
            grouped_paths.append(path_points)
            print("Found Path")
    return grouped_paths

# Preview each path in a different color
def preview_points(paths):
    plt.figure(figsize=(8, 6))
    colors = plt.cm.get_cmap('tab10', len(paths))
    for i, path in enumerate(paths):
        xs, ys = zip(*path)
        plt.plot(xs, ys, marker='.', linestyle='-', color=colors(i), label=f"Path {i+1}")
    plt.gca().invert_yaxis()
    plt.axis('equal')
    plt.title("V-Plotter SVG Paths Preview")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Draw each path with pen lifted between paths
def draw_points(ser, path_groups):
    home_x, home_y = 200, 200
    initial_left_steps, initial_right_steps = coords_to_steps(home_x, home_y)

    pen_lift(True)  # start lifted

    for path in path_groups:
        if not path:
            continue

        # Move to the start of the path
        start_x, start_y = path[0]
        left, right = coords_to_steps(start_x, start_y)
        ser.write(f"{left - initial_left_steps},{initial_right_steps - right}\n".encode())
        time.sleep(8) # wait for the pen to get to its destination coordinate
        
        pen_lift(False)  # lower pen to draw

        for x, y in path:
            left, right = coords_to_steps(x, y)
            ser.write(f"{left - initial_left_steps},{initial_right_steps - right}\n".encode())
            time.sleep(0.3)

        pen_lift(True)  # lift after each path

    # Return to home
    left_steps, right_steps = coords_to_steps(home_x, home_y)
    ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())

# Main
if __name__ == "__main__":
    svg_file = "try.svg"
    paths = sample_svg_path(svg_file, scale=1, offset_x=200, offset_y=300)

    preview_points(paths)

    with serial.Serial('COM4', 115200, timeout=1) as ser:
        time.sleep(2)
        draw_points(ser, paths)
