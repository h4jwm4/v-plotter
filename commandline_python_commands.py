for i in np.arange(0, 50, 0.5):  # 100 steps along the line
        x = 300 + i
        y = 300 + i
        left_steps, right_steps = coords_to_steps(x, y)
        ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
        time.sleep(0.3)

for i in np.arange(0, 50, 0.5):  # 100 steps along the line
        x = 354.5 - i
        y = 349.5 - i
        left_steps, right_steps = coords_to_steps(x, y)
        ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
        time.sleep(0.3)

ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}, 0\n".encode())
time.sleep(2)
for i in np.arange(0, 50, 0.5):  # 100 steps along the line
        x = 310.0 + i
        y = 300 + i
        left_steps, right_steps = coords_to_steps(x, y)
        ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
        time.sleep(0.3)

ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}, 20\n".encode())

left_steps, right_steps = coords_to_steps(x+5, y)
//364.5

ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}, 0\n".encode())

for i in np.arange(0, 50, 0.5):  # 100 steps along the line
        x = 364.5 - i
        y = 349.5 - i
        left_steps, right_steps = coords_to_steps(x, y)
        ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
        time.sleep(0.3)


for i in np.arange(0, 50, 0.5):  # 100 steps along the line
        x = 364.5 + i
        left_steps, right_steps = coords_to_steps(x, y)
        ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
        time.sleep(0.3)

for i in np.arange(0, 150, 0.5):  # 100 steps along the line
        x = x - i
        left_steps, right_steps = coords_to_steps(x, y)
        ser.write(f"{left_steps - initial_left_steps},{initial_right_steps - right_steps}\n".encode())
        time.sleep(0.3)