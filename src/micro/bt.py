import aioble
from machine import Pin

class BT():
    def __init__(self, service_uuid, char_uuid, char_appearance, adv_interval):
        self._service_uuid = service_uuid
        self._char_appearance = char_appearance
        self._adv_interval = adv_interval
        service = aioble.Service(service_uuid)
        aioble.Characteristic(service, char_uuid, read=True, notify=True)
        aioble.register_services(service)

    async def connect(self, led_gpio: int):
        led = Pin(id=led_gpio, mode=Pin.OUT)
        led.value(0)
        while True:
            async with await aioble.advertise(
                self._adv_interval,
                name="temp-sense",
                services=[self._service_uuid],
                appearance=self._char_appearance,
            ) as connection: #type: ignore
                led.value(1)
                await connection.disconnected(timeout_ms=None)
                led.value(0)