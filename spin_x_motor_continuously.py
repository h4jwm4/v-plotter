import tkinter as tk
from tkinter import ttk
import serial
import time

# --- Serial Config ---
ser = serial.Serial('COM4', 115200)
time.sleep(2)

# --- Commands ---
def set_speed(val):
    speed = float(val)
    ser.write(f"SPEED:{speed}\n".encode())

def set_accel(val):
    accel = float(val)
    ser.write(f"ACCEL:{accel}\n".encode())

def start_motor():
    ser.write(b"START\n")

def stop_motor():
    ser.write(b"STOP\n")

# --- GUI Setup ---
root = tk.Tk()
root.title("Stepper Motor Control")

tk.Label(root, text="Max Speed").pack()
speed_slider = ttk.Scale(root, from_=1000, to=1000000, orient="horizontal", command=set_speed)
speed_slider.set(500)
speed_slider.pack()

tk.Label(root, text="Acceleration").pack()
accel_slider = ttk.Scale(root, from_=1000, to=10000, orient="horizontal", command=set_accel)
accel_slider.set(200)
accel_slider.pack()

tk.Button(root, text="Start", command=start_motor).pack(pady=10)
tk.Button(root, text="Stop", command=stop_motor).pack(pady=5)

root.mainloop()
