from math import log

def convert_temp_f(adc_data: list[int], v_ref: float, adc_bitsize: int, resistance_at_25C: int, series_resistance: int, beta: int, is_pull_down: bool) -> list[float]:
    temps_f = []
    voltage_factor = v_ref / ((2 ** adc_bitsize)-1)

    for adc in adc_data:
        voltage = adc * voltage_factor
        if is_pull_down:
            res = (voltage / (v_ref - voltage)) * series_resistance
        else:
            res = ((v_ref - voltage) / voltage) * series_resistance
        temp_c = (beta / (log(res / resistance_at_25C) + (beta / 298))) - 273
        temps_f.append((temp_c * 9/5) + 32)

    return temps_f