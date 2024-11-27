import numpy
from scipy.optimize import curve_fit
from math import log

def convert_temp_f(adc: int, v_ref: float, adc_bitsize: int, series_resistance: int, beta: int, is_pull_down: bool) -> float:
    
    voltage_factor = v_ref / ((2 ** adc_bitsize)-1)
    voltage = adc * voltage_factor
    if is_pull_down:
        res = (voltage / (v_ref - voltage)) * series_resistance
    else:
        res = ((v_ref - voltage) / voltage) * series_resistance

    temp_c = (beta / (log(res / series_resistance) + (beta / 298))) - 273
    return (temp_c * 9/5) + 32

def _decay_func(t, a, b, amb_temp):
    return a * numpy.exp(-b * t) + amb_temp

def get_decay_params(data: list[int], sample_period_s) -> tuple[float, float, float]:
    time = numpy.array([float(t*sample_period_s) for t in range(0, len(data))])
    temp = numpy.array(data)

    params, _ = curve_fit(_decay_func, time, temp)
    a, b, amb_temp = params
    
    return a, b, amb_temp