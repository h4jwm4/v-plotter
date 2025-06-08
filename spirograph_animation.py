import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def spirograph(R, r, d, spacing_mm=0.05):
    """
    Generate spirograph points with approx. spacing_mm resolution in mm.
    """
    # Estimate full length to determine number of points
    max_circumference = 2 * np.pi * R * 10  # overdraw to ensure full pattern
    num_points = int(max_circumference / spacing_mm)
    t = np.linspace(0, 2 * np.pi * 10, num_points)  # 10 revolutions

    x = (R - r) * np.cos(t) + d * np.cos(((R - r) / r) * t)
    y = (R - r) * np.sin(t) - d * np.sin(((R - r) / r) * t)
    return x, y

def animate_spirograph(x, y, interval=-1000):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_xlim(min(x)-10, max(x)+10)
    ax.set_ylim(min(y)-10, max(y)+10)
    ax.set_title("Spirograph Animation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    line, = ax.plot([], [], lw=1.5, color='darkblue')

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        line.set_data(x[:frame], y[:frame])
        return line,

    ani = animation.FuncAnimation(
        fig, update, frames=len(x), init_func=init,
        blit=True, interval=interval, repeat=False
    )

    plt.show()

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

# Example usage
if __name__ == "__main__":
    R = 100  # outer radius
    r = 30   # inner radius
    d = 60   # pen offset
    spacing_mm = 0.05

    x, y = spirograph(R=83.5*0.5, r=8.0*0.5, d=49.5*0.5, spacing_mm=0.05)
    #animate_spirograph(x, y)
    preview_points(zip(x, y))
