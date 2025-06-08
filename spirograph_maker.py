import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def spirograph(R, r, d, revolutions=10, resolution=2000):
    t = np.linspace(0, 2 * np.pi * revolutions, resolution)
    x = (R - r) * np.cos(t) + d * np.cos(((R - r) / r) * t)
    y = (R - r) * np.sin(t) - d * np.sin(((R - r) / r) * t)
    return x, y

class SpirographApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spirograph Generator")

        # Create sliders
        self.create_sliders()

        # Create plot
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=4)

        self.update_plot()

    def create_sliders(self):
        self.slider_frame = tk.Frame(self.root)
        self.slider_frame.grid(row=0, column=0, sticky='ns')

        self.R_var = tk.DoubleVar(value=100)
        self.r_var = tk.DoubleVar(value=30)
        self.d_var = tk.DoubleVar(value=60)

        sliders = [
            ("R (fixed circle radius)", self.R_var, 10, 200),
            ("r (rolling circle radius)", self.r_var, 5, 100),
            ("d (pen offset)", self.d_var, 0, 200)
        ]

        for i, (label, var, min_val, max_val) in enumerate(sliders):
            tk.Label(self.slider_frame, text=label).grid(row=i*2, column=0, sticky='w', pady=(10, 0))
            slider = ttk.Scale(self.slider_frame, from_=min_val, to=max_val,
                               variable=var, orient='horizontal', length=200, command=self.on_slider_change)
            slider.grid(row=i*2+1, column=0, pady=(0, 10))

    def on_slider_change(self, _):
        self.update_plot()

    def update_plot(self):
        R = self.R_var.get()
        r = self.r_var.get()
        d = self.d_var.get()
        self.ax.clear()

        x, y = spirograph(R, r, d)
        self.ax.plot(x, y, color='blue')
        self.ax.set_aspect('equal')
        self.ax.set_title(f"Spirograph (R={R:.1f}, r={r:.1f}, d={d:.1f})")
        self.ax.grid(True)

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpirographApp(root)
    root.mainloop()
