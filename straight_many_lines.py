import serial
import time
import math
import numpy as np

# Plotter dimensions
MOTOR_DISTANCE = 779.0  # mm
STEP_SIZE = 0.04        # mm per step at 1/4 microstepping

# Function to convert (x, y) to motor steps
def coords_to_steps(x, y):
    left_length = math.hypot(x, y)
    right_length = math.hypot(MOTOR_DISTANCE - x, y)
    left_steps = int(left_length / STEP_SIZE)
    right_steps = int(right_length / STEP_SIZE)
    return left_steps, right_steps

# Example: draw a diagonal line from (100, 100) to (200, 200)
with serial.Serial('COM4', 115200, timeout=1) as ser:
    time.sleep(2)  # wait for Arduino to reset
    ser.write(f"0,0,0\n".encode())
    input("Enter")
    initial_left_steps, initial_right_steps = coords_to_steps(200, 200)
    prev_x = 200
    prev_y = 200
    for i in range(19):
        if i != 0:
            for i in np.arange(0, 3, 0.5):  # 100 steps along the line
                y = prev_y + i
                left_steps, right_steps = coords_to_steps(x, y)
                ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
                time.sleep(0.3)
            prev_x = x
            prev_y = y
        for i in np.arange(0, 100, 0.5):  # 100 steps along the line
            x = prev_x + i
            y = prev_y
            left_steps, right_steps = coords_to_steps(x, y)
            ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
            time.sleep(0.3)  # tune for speed/smoothness
        prev_x = x
        prev_y = y
        for i in np.arange(0, 3, 0.5):  # 100 steps along the line
            y = prev_y + i
            left_steps, right_steps = coords_to_steps(x, y)
            ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
            time.sleep(0.3)  # tune for speed/smoothness
        prev_x = x
        prev_y = y
        for i in np.arange(0, 100, 0.5):  # 100 steps along the line
            x = prev_x - i
            left_steps, right_steps = coords_to_steps(x, y)
            ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
            time.sleep(0.3)  # tune for speed/smoothness
        prev_x = x