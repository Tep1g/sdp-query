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