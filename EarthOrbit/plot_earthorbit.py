# plot_mercpert.py
import matplotlib.pyplot as plt

def plot_mercpert(data):
    xsSun, ysSun = data["sun"]
    xsPlanet, ysPlanet = data["planet"]
    xsMerc, ysMerc = data["mercury"]

    plt.figure(figsize=(8,8))
    plt.plot(xsSun, ysSun, 'r-', label="Sun")
    plt.plot(xsPlanet, ysPlanet, 'g-', label="Planet")
    plt.plot(xsMerc, ysMerc, 'b-', label="Mercury")

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("MercPert orbits (non‑RK45)")
    plt.legend()
    plt.axis('equal')
    plt.grid(True)
    plt.show()
