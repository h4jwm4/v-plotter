import math
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import threading
import msvcrt
from svgpathtools import svg2paths2

# V-Plotter constants
pause_flag = False
home_flag = False
MOTOR_DISTANCE = 779.0  # mm
STEP_SIZE = 0.005       # mm per step
delay_time = 0.025 

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
# Convert (x, y) to motor steps
def coords_to_steps(x, y):
    left_length = math.hypot(x, y)
    right_length = math.hypot(MOTOR_DISTANCE - x, y)
    left_steps = int(left_length / STEP_SIZE)
    right_steps = int(right_length / STEP_SIZE)
    return left_steps, right_steps

def pen_lift(ser, lift=True):
    if lift:
        for angle in range(180, 75, -1):
            command = f"S:{angle}\n"
            ser.write(command.encode())
            time.sleep(0.02)
    else:
        for angle in range(75, 180, 1):
            command = f"S:{angle}\n"
            ser.write(command.encode())
            time.sleep(0.02)


"""
# Sample SVG file into points
def sample_svg_path(svg_file, spacing_mm=0.05, scale=1.0, offset_x=0, offset_y=0):
    paths, attributes, svg_attributes = svg2paths2(svg_file)
    all_paths = []

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
            all_paths.append(path_points)
    return all_paths

"""
def sample_svg_path(svg_file, spacing_mm=0.05, scale=1.0, offset_x=0, offset_y=0, gap_threshold=0.5):
    paths, attributes, svg_attributes = svg2paths2(svg_file)
    all_paths = []

    for path in paths:
        current_path = []
        last_point = None
        for segment in path:
            scaled_length = segment.length() * scale
            num_samples = max(1, int(scaled_length / spacing_mm))
            for i in range(num_samples + 1):
                t = i / num_samples
                point = segment.point(t)
                x = (point.real * scale) + offset_x
                y = (point.imag * scale) + offset_y

                if last_point:
                    gap = math.hypot(x - last_point[0], y - last_point[1])
                    if gap > gap_threshold:
                        # Finish current sub-path and start a new one
                        if current_path:
                            all_paths.append(current_path)
                        current_path = []

                current_path.append((x, y))
                last_point = (x, y)

        # After all segments in this path
        if current_path:
            all_paths.append(current_path)

    return all_paths


# Preview sampled points using matplotlib
def preview_points(points):
    xs, ys = zip(*points)
    plt.figure(figsize=(8, 6))
    plt.plot(xs, ys, marker='.', linestyle='-', color='black')
    plt.gca().invert_yaxis()  # SVG y-axis is top-down
    plt.axis('equal')
    plt.title("V-Plotter SVG Preview")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)
    plt.show()
    

def preview_paths(paths):
    plt.figure(figsize=(8, 6))
    for path in paths:
        xs, ys = zip(*path)
        plt.plot(xs, ys, marker='.', linestyle='-')
    plt.gca().invert_yaxis()
    plt.axis('equal')
    plt.title("Separated SVG Paths Preview")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)
    plt.show()

"""
# Send drawing commands to Arduino
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
    input("[*] Enter to Return to Home")
    left_steps, right_steps = coords_to_steps(200, 200)
    ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode()) # return to home position (200,200)
"""

def wait_for_done(ser, expected_x, expected_y, timeout=10):
    """
    Waits for the Arduino to send 'DONE: x, y' over serial.

    Parameters:
        ser (serial.Serial): An open serial connection
        expected_x (int): Expected X coordinate in steps
        expected_y (int): Expected Y coordinate in steps
        timeout (float): How long to wait (seconds) before giving up

    Returns:
        bool: True if correct DONE received, False if timeout occurred
    """
    expected_message = f"DONE: {expected_x}, {expected_y}"
    start_time = time.time()
    while True:
        if ser.in_waiting:
            response = ser.readline().decode(errors='ignore').strip()
            print(f"[Arduino] {response}")
            if response == expected_message:
                print("[✓] Movement completed to expected position.")
                return True
        if time.time() - start_time > timeout:
            print("[!] Timeout waiting for DONE.")
            return False
        time.sleep(0.01)
"""
def draw_points(ser, paths):
    global pause_flag, home_flag, delay_time

    # Start keyboard listener in background
    listener = threading.Thread(target=keyboard_listener, daemon=True)
    listener.start()

    pen_lift(True)
    home_left, home_right = coords_to_steps(200, 200)
    input("[+] Enter to Start: ")

    for path_index, points in enumerate(paths):
        if not points:
            continue

        # Move to the start of the path with pen up
        first_x, first_y = points[0]
        left, right = coords_to_steps(first_x, first_y)
        ser.write(f"{left - home_left},{home_right - right}\n".encode())
        print(f"[*] Moved to start of path {path_index + 1}")
        #input("[*] Press ENTER to drop pen and draw this path...")
        wait_for_done(ser, left - home_left, home_right - right, timeout=100)
        # Pen down and draw path
        pen_lift(False)
        for x, y in points:
            if home_flag:
                break
            while pause_flag:
                time.sleep(0.1)
            left, right = coords_to_steps(x, y)
            ser.write(f"{left - home_left},{home_right - right}\n".encode())
            time.sleep(0.05)
        pen_lift(True)
        print(f"[*] Path {path_index + 1} completed.")

    if home_flag:
        print("[*] Sending machine to home...")

    input("[+] Return to home. Press Enter...")
    ser.write(f"{home_left - home_left},{home_right - home_right}\n".encode())
"""
"""
def draw_points(ser, paths):
    global pause_flag, home_flag, delay_time

    listener = threading.Thread(target=keyboard_listener, daemon=True)
    listener.start()

    pen_lift(ser, True)
    home_left, home_right = coords_to_steps(200, 200)
    input("[+] Enter to Start: ")

    last_point = None

    for path_index, points in enumerate(paths):
        if not points:
            continue

        for i, (x, y) in enumerate(points):
            if home_flag:
                break
            while pause_flag:
                time.sleep(0.1)

            left, right = coords_to_steps(x, y)

            if i == 0:
                # Beginning of new path segment
                if last_point:
                    # Check if there's a gap between last_point and this start point
                    gap = math.hypot(x - last_point[0], y - last_point[1])
                    print(gap)
                    if gap > 0.5:  # If distance > 0.5mm, lift and move
                        pen_lift(ser, True)
                        print("Penlift True")
                        ser.write(f"{left - home_left},{home_right - right}\n".encode())
                        wait_for_done(ser, left - home_left, home_right - right, timeout=100)
                        pen_lift(ser, False)
                    else:
                        # Treat as continuation without lifting
                        pass
                else:
                    # First-ever point
                    pen_lift(ser, True)
                    ser.write(f"{left - home_left},{home_right - right}\n".encode())
                    wait_for_done(ser, left - home_left, home_right - right, timeout=100)
                    pen_lift(ser, False)
            else:
                # Intermediate path point
                ser.write(f"{left - home_left},{home_right - right}\n".encode())
                time.sleep(delay_time)

            last_point = (x, y)

        pen_lift(ser, True)
        print(f"[*] Path {path_index + 1} completed.")

    if home_flag:
        print("[*] Sending machine to home...")

    input("[+] Return to home. Press Enter...")
    ser.write(f"{home_left - home_left},{home_right - home_right}\n".encode())
"""

def draw_points(ser, paths):
    global pause_flag, home_flag, delay_time

    listener = threading.Thread(target=keyboard_listener, daemon=True)
    listener.start()

    pen_lift(ser, True)
    home_left, home_right = coords_to_steps(200, 200)
    input("[+] Enter to Start: ")

    last_point = None
    first_move = True

    for path_index, points in enumerate(paths):
        if not points:
            continue

        start_x, start_y = points[0]
        left, right = coords_to_steps(start_x, start_y)

        if first_move:
            pen_lift(ser, True)
            ser.write(f"{left - home_left},{home_right - right}\n".encode())
            wait_for_done(ser, left - home_left, home_right - right, timeout=100)
            pen_lift(ser, False)
            first_move = False
        else:
            gap = math.hypot(start_x - last_point[0], start_y - last_point[1])
            if gap > 0.5:
                pen_lift(ser, True)
                print(f"[*] Moving with pen lift: gap = {gap:.2f}")
                ser.write(f"{left - home_left},{home_right - right}\n".encode())
                wait_for_done(ser, left - home_left, home_right - right, timeout=100)
                pen_lift(ser, False)
            else:
                # No pen lift, just continue
                ser.write(f"{left - home_left},{home_right - right}\n".encode())
                wait_for_done(ser, left - home_left, home_right - right, timeout=100)

        # Now draw remaining points of this path (skip the first point)
        for x, y in points[1:]:
            if home_flag:
                break
            while pause_flag:
                time.sleep(0.1)

            left, right = coords_to_steps(x, y)
            ser.write(f"{left - home_left},{home_right - right}\n".encode())
            time.sleep(delay_time)

            last_point = (x, y)

        print(f"[*] Path {path_index + 1} completed.")
        last_point = points[-1]  # Track last point for gap logic

    if home_flag:
        print("[*] Sending machine to home...")
    pen_lift(ser, True)
    input("[+] Return to home. Press Enter...")
    ser.write(f"{home_left - home_left},{home_right - home_right}\n".encode())


# Main
if __name__ == "__main__":
    # svg_file = "line-svgrepo-comv2.svg"  # your file
    svg_file = "superb_craft.svg"
    #points = sample_svg_path(svg_file, scale=1, offset_x=200, offset_y=200)

    # Preview the drawing
    #preview_points(points)
    paths = sample_svg_path(svg_file, scale=0.05, offset_x=200, offset_y=200)
    preview_points([pt for path in paths for pt in path]) 
    preview_paths(paths)

    with serial.Serial('COM4', 115200, timeout=1) as ser:
        time.sleep(2)
        draw_points(ser, paths)