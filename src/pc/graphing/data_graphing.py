import numpy as np
import matplotlib.pyplot as plt

def plot_temp_func(duration_s: int, a: float, b: float, T_amb: float):
    t = np.linspace(0, duration_s, duration_s * 10)
    temp = a*np.exp(-b*t) + T_amb

    plt.plot(t, temp)
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.title('Temperature Function')
    plt.grid(True)
    plt.show()