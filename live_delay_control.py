import serial
import time
import math
import numpy as np
import threading
import tkinter as tk

# Plotter constants
MOTOR_DISTANCE = 779.0  # mm
STEP_SIZE = 0.04        # mm per step

# Shared delay variable (in seconds)
delay = 0.5

# Function to convert (x, y) to motor steps
def coords_to_steps(x, y):
    left_length = math.hypot(x, y)
    right_length = math.hypot(MOTOR_DISTANCE - x, y)
    left_steps = int(left_length / STEP_SIZE)
    right_steps = int(right_length / STEP_SIZE)
    return left_steps, right_steps

# Function to update delay from slider (in ms)
def update_delay(val):
    global delay
    delay = max(0.001, int(val) / 1000.0)  # Convert ms to seconds
    label_var.set(f"Delay: {int(val)} ms")

# Tkinter GUI in a thread
def start_gui():
    global label_var
    root = tk.Tk()
    root.title("Plotter Speed Control")

    tk.Label(root, text="Adjust drawing delay (ms)").pack(pady=10)

    slider = tk.Scale(root, from_=1, to=1000, orient=tk.HORIZONTAL, command=update_delay)
    slider.set(int(delay * 1000))
    slider.pack(padx=20)

    label_var = tk.StringVar()
    label_var.set(f"Delay: {int(delay * 1000)} ms")
    tk.Label(root, textvariable=label_var).pack(pady=5)

    root.mainloop()

# Launch GUI in background thread
threading.Thread(target=start_gui, daemon=True).start()

# Main V-Plotter loop
with serial.Serial('COM4', 115200, timeout=1) as ser:
    time.sleep(2)  # Allow Arduino to reset

    initial_left_steps, initial_right_steps = coords_to_steps(200, 200)
    for i in np.arange(0, 500, 0.1):
        x = 200 + i
        y = 200
        left_steps, right_steps = coords_to_steps(x, y)
        delta_left = left_steps - initial_left_steps
        delta_right = initial_right_steps - right_steps
        ser.write(f"{delta_left},{delta_right}\n".encode())

        time.sleep(delay)  # Live-controlled delay
