import aioble
import asyncio
import bluetooth
from machine import Pin
from sense import Sensor

# Device name
DEVICE_NAME = "temp-sense"

# Custom service
SERVICE_UUID = bluetooth.UUID(0x9999)

# org.bluetooth.characteristic.analog
ANALOG_UUID = bluetooth.UUID(0x25A8)

# org.bluetooth.characteristic.gap.appearance.xml
GATT_APPEARANCE_GENERIC_SENSOR = const(1344)

ADV_INTERVAL_US = const(250000)

LED_GPIO = const(16)
ADC_PORT = const(2)
SAMPLING_RATE_MS = const(500)
TIMER_ID = const(-1)

async def main():
    service = aioble.Service(SERVICE_UUID)
    characteristic = aioble.Characteristic(service, ANALOG_UUID, read=True, notify=True)
    aioble.register_services(service)

    Sensor(adc_port=ADC_PORT, sampling_rate_ms=SAMPLING_RATE_MS, timer_id=TIMER_ID, bt_char=characteristic)

    led = Pin(LED_GPIO, Pin.OUT)
    led.value(0)
    while True:
        async with await aioble.advertise(
            ADV_INTERVAL_US,
            name=DEVICE_NAME,
            services=[SERVICE_UUID],
            appearance=GATT_APPEARANCE_GENERIC_SENSOR,
        ) as connection: #type: ignore
            led.value(1)
            await connection.disconnected(timeout_ms=None)
            led.value(0)

if __name__ == "__main__":
    asyncio.run(main())