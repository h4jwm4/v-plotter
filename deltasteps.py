import serial
import time
import math

# Your machine's physical settings
MOTOR_DISTANCE_MM = 779
STEPS_PER_REV = 200
MICROSTEPPING = 4
PULLEY_TEETH = 16
BELT_PITCH_MM = 2

STEPS_PER_MM = (STEPS_PER_REV * MICROSTEPPING) / (PULLEY_TEETH * BELT_PITCH_MM)

# Convert XY to motor string lengths
def coords_to_lengths(x, y):
    left_len = math.hypot(x, y)
    right_len = math.hypot(MOTOR_DISTANCE_MM - x, y)
    return left_len, right_len

# Convert delta XY to delta motor steps
def coords_to_steps(x0, y0, x1, y1):
    l0, r0 = coords_to_lengths(x0, y0)
    l1, r1 = coords_to_lengths(x1, y1)
    dl = (l1 - l0) * STEPS_PER_MM
    dr = (r1 - r0) * STEPS_PER_MM
    return round(dl), round(dr)

# Send line from (x0, y0) to (x1, y1)
def draw_line(x0, y0, x1, y1, ser, steps=100, delay=0.01):
    for i in range(1, steps + 1):
        xi = x0 + (x1 - x0) * i / steps
        yi = y0 + (y1 - y0) * i / steps
        dx, dy = coords_to_steps(x0, y0, xi, yi)
        x0, y0 = xi, yi
        ser.write(f"{dx},{dy}\n".encode())
        time.sleep(delay)

# Run drawing
with serial.Serial("COM4", 115200, timeout=1) as ser:
    time.sleep(2)
    draw_line(200, 200, 100, 100, ser)
