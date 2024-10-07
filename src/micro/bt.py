import aioble
from bluetooth import UUID
from machine import Pin

class BT():
    def __init__(self, device_name: str, service_uuid: UUID, char_uuid: UUID, char_appearance: int, adv_interval: int):
        self._device_name = device_name
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
                name=self._device_name,
                services=[self._service_uuid],
                appearance=self._char_appearance,
            ) as connection: #type: ignore
                led.value(1)
                await connection.disconnected(timeout_ms=None)
                led.value(0)