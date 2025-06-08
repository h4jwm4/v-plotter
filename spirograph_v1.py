import numpy as np
import matplotlib.pyplot as plt
import math
import serial
import threading
import msvcrt
import time

# V-Plotter constants
MOTOR_DISTANCE = 779.0  # mm
STEP_SIZE = 0.005       # mm per step

pause_flag = False
home_flag = False
delay_time = 0.25 

def keyboard_listener():
    global pause_flag, home_flag, delay_time
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').upper()
            if key == 'P':
                pause_flag = not pause_flag
                print("[*] Paused" if pause_flag else "[*] Resumed")
            elif key == 'H':
                home_flag = True
                print("[*] Returning to Home")
            elif key == 'J':
                delay_time = max(0.01, delay_time - 0.05)
                print(f"[+] Speed increased. Delay: {delay_time:.2f} sec")
            elif key == 'L':
                delay_time += 0.05
                print(f"[-] Speed decreased. Delay: {delay_time:.2f} sec")
        time.sleep(0.05)

def draw_points(ser, points):
    global pause_flag, home_flag, delay_time

    # Start keyboard listener in background
    listener = threading.Thread(target=keyboard_listener, daemon=True)
    listener.start()

    pen_lift(True)
    initial_left_steps, initial_right_steps = coords_to_steps(200, 200)

    left, right = coords_to_steps(*points[0])
    ser.write(f"{left - initial_left_steps},{initial_right_steps - right}\n".encode())
    input("Enter to start drawing:")

    pen_lift(False)

    for x, y in points:
        if home_flag:
            break
        while pause_flag:
            time.sleep(0.1)

        left, right = coords_to_steps(x, y)
        ser.write(f"{left - initial_left_steps},{initial_right_steps - right}\n".encode())
        time.sleep(delay_time)  # Use adjustable delay  # Adjust for speed/smoothness

    pen_lift(True)

    if home_flag:
        print("[*] Sending machine to home...")

    input("[+] Return to home. Press Enter...")

    left_steps, right_steps = coords_to_steps(200, 200)
    ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())

def coords_to_steps(x, y):
    left_length = math.hypot(x, y)
    right_length = math.hypot(MOTOR_DISTANCE - x, y)
    left_steps = int(left_length / STEP_SIZE)
    right_steps = int(right_length / STEP_SIZE)
    return left_steps, right_steps

def spirograph_mm(R, r, d, spacing_mm=0.05, scale=1.0, offset_x=0, offset_y=0):
    """
    Generate spirograph (hypotrochoid) points spaced approximately every `spacing_mm` mm.
    """
    # Estimate total arc length to determine how many samples needed
    total_revolutions = 10
    num_samples = int((2 * np.pi * R * total_revolutions) / spacing_mm)
    t = np.linspace(0, 2 * np.pi * total_revolutions, num_samples)
    x = (R - r) * np.cos(t) + d * np.cos(((R - r) / r) * t)
    y = (R - r) * np.sin(t) - d * np.sin(((R - r) / r) * t)

    # Apply scaling and offset
    x = x * scale + offset_x
    y = y * scale + offset_y

    return list(zip(x, y))

def preview_points(points):
    xs, ys = zip(*points)
    plt.figure(figsize=(8, 8))
    plt.plot(xs, ys, marker='.', linestyle='-', color='darkblue')
    plt.gca().set_aspect('equal')
    plt.title("Spirograph V-Plotter Preview")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)
    plt.gca().invert_yaxis()  # Invert Y to match V-Plotter behavior
    plt.show()

# Send drawing commands to Arduino
'''
def draw_points(ser, points):
    pen_lift(True)
    initial_left_steps, initial_right_steps = coords_to_steps(200, 200)

    left, right = coords_to_steps(*points[0])
    ser.write(f"{left - initial_left_steps},{initial_right_steps - right}\n".encode())
    input("Enter to continue:")

    pen_lift(False) # intitate the pen to the paper
    for x, y in points[0:]:
        left, right = coords_to_steps(x, y)

        ser.write(f"{left - initial_left_steps},{initial_right_steps - right}\n".encode())
        time.sleep(0.05)  # tune for speed/smoothness
    pen_lift(True) # lift the pen
    input("[+]Return to home: ")
    left_steps, right_steps = coords_to_steps(200, 200)
    ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode()) # return to home position (200,200)
'''

def pen_lift(lift=True):
    if lift:
        # Send servo from 90 to 20 degrees smoothly
        for angle in range(130, 81, -1):  # From 90 down to 20
            command = f"S:{angle}\n"   # X=0, Y=0, Servo=angle
            ser.write(command.encode())
            time.sleep(0.02)  # 20 ms delay for smooth motion
    else:
        # Optional: go back u
        for angle in range(80, 131, 1):
            command = f"S:{angle}\n"
            ser.write(command.encode())
            time.sleep(0.02)

def generate_line_points(x_end, y_end, spacing=1.0):
    """
    Generate points from (200, 200) to (x_end, y_end) with given spacing.

    Args:
        x_end (float): Destination x-coordinate
        y_end (float): Destination y-coordinate
        spacing (float): Distance between consecutive points in mm

    Returns:
        list of (x, y) tuples
    """
    x_start, y_start = 200, 200
    dx = x_end - x_start
    dy = y_end - y_start
    distance = np.hypot(dx, dy)

    # Number of points based on total distance and spacing
    num_points = max(1, int(distance / spacing))
    
    # Linearly interpolate x and y
    x = np.linspace(x_start, x_end, num_points + 1)
    y = np.linspace(y_start, y_end, num_points + 1)
    
    return list(zip(x, y))

# Main
if __name__ == "__main__":
    # Generate and preview spirograph
    points = spirograph_mm(R=83.5*0.5, r=8.0*0.5, d=49.5*0.5, spacing_mm=0.05, offset_x=300, offset_y=300)
    #points = generate_line_points(450, 200, spacing=0.05)

    preview_points(points)
    with serial.Serial('COM4', 115200, timeout=1) as ser:
        time.sleep(2)
        draw_points(ser, points)


