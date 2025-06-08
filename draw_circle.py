import serial
import time
import math

# Plotter dimensions
MOTOR_DISTANCE = 779.0  # mm
STEP_SIZE = 0.005     # mm per step at 1/4 microstepping

# Function to convert (x, y) to motor steps
def coords_to_steps(x, y):
    left_length = math.hypot(x, y)
    right_length = math.hypot(MOTOR_DISTANCE - x, y)
    left_steps = int(left_length / STEP_SIZE)
    right_steps = int(right_length / STEP_SIZE)
    return left_steps, right_steps


def draw_circle(ser, cx, cy, radius, num_points=100):
    """
    Draw a circle using the V plotter.

    :param ser: Serial object connected to the Arduino
    :param cx: X coordinate of the circle center
    :param cy: Y coordinate of the circle center
    :param radius: Radius of the circle (in mm)
    :param num_points: Number of points to use for the circle
    """
    angle_step = 2 * math.pi / num_points

    # Generate the initial point
    x = cx + radius * math.cos(0)
    y = cy + radius * math.sin(0)
    initial_left_steps, initial_right_steps = coords_to_steps(300, 300)

    left_steps, right_steps = coords_to_steps(x,y)
    ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
    input("Enter to continue:")
    
    for i in range(1, num_points + 1):
        angle = i * angle_step
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)

        left_steps, right_steps = coords_to_steps(x, y)

        ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
        time.sleep(0.03)  # Adjust for smoothness

with serial.Serial('COM4', 115200, timeout=1) as ser:
    time.sleep(2)  # allow Arduino to reset
    draw_circle(ser, cx=300, cy=300, radius=50, num_points=629)