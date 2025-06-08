import serial
import time

def wait_for_done(ser, timeout=10):
    """
    Waits for the Arduino to send 'DONE' over serial.
    
    Parameters:
        ser (serial.Serial): An open serial connection
        timeout (float): How long to wait (seconds) before giving up

    Returns:
        bool: True if DONE received, False if timeout occurred
    """
    start_time = time.time()
    while True:
        if ser.in_waiting:
            response = ser.readline().decode(errors='ignore').strip()
            print(f"[Arduino] {response}")
            if response == "DONE":
                print("[✓] Movement completed.")
                return True
        if time.time() - start_time > timeout:
            print("[!] Timeout waiting for DONE.")
            return False
        time.sleep(0.01)  # prevent CPU hogging

with serial.Serial('COM4', 115200, timeout=1) as ser:
    time.sleep(2)  # Let Arduino reset

    ser.write(b"2000,2000\n")  # Send movement command
    wait_for_done(ser, timeout=10)