import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def _decay_func(t, a, b, amb_temp):
    return a * np.exp(-b * t) + amb_temp

def _get_decay_params(data: list[float], sample_period_s) -> tuple[float, float, float]:
    time = np.array([float(t*sample_period_s) for t in range(0, len(data))])
    temp = np.array(data)

    params, _ = curve_fit(_decay_func, time, temp)
    a, b, amb_temp = params
    
    return a, b, amb_temp

def plot_temp_exp_decay(data: list[float], duration_s: int):
    sample_period_s = duration_s / len(data)
    a, b, amb_temp = _get_decay_params(data, sample_period_s)
    function_string = "{:.2f}*exp(-{:.5f}*t) + {:.2f}".format(a, b, amb_temp)
    print(function_string)
    t = np.linspace(0, duration_s, duration_s * 10)
    temp = a*np.exp(-b*t) + amb_temp

    plt.plot(t, temp)
    plt.xlabel('Time (seconds)', fontsize=16)
    plt.ylabel('Temperature (degF)', fontsize=16)
    plt.title('Curve Fit Function: {}'.format(function_string))
    plt.grid(True)
    plt.show()

def plot_temps(data: list[float], duration_s: int):
    sample_period_s = duration_s / len(data)
    time = np.array([float(t*sample_period_s) for t in range(0, len(data))])
    temp = np.array(data)

    plt.plot(time, temp)
    plt.xlabel('Time (seconds)', fontsize=16)
    plt.ylabel('Temperature (degF)', fontsize=16)
    plt.grid(True)
    plt.show()
