from aioble import Characteristic
from machine import ADC, Timer

class Sensor:
    def __init__(self, adc_port: int, sampling_rate_ms: int, timer_id:int, bt_char: Characteristic):
        self._adc = ADC(adc_port)
        self._bt_char = bt_char
        self._timer = Timer(timer_id)
        self._timer.init(mode=Timer.PERIODIC, period=sampling_rate_ms, callback=self._callback_send)

    def _callback_send(self, timer):
        self._bt_char.write((self._adc.read_u16()).to_bytes(2, 'little', False)) # type: ignore