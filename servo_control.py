import serial
import time

# Replace 'COM3' with your Arduino port (e.g., '/dev/ttyUSB0' on Linux)
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

# Example command: Move to (1000, 500) and rotate servo to 90°
command = f"1000,500,90\n"
ser.write(command.encode())

# Optional: wait and send another
time.sleep(2)
ser.write(f"0,0,0\n".encode())
