import asyncio
import time
from bleak import BleakScanner, BleakClient

_ANALOG_UUID = "000025a8-0000-1000-8000-00805f9b34fb"

class SensorBT():
    def __init__(self):
        self.data = []
        self._sensor_address = None

    def _data_callback(self, sender, data):
        self.data.append(int.from_bytes(bytes=data, byteorder='little', signed=False))

    async def connect(self):
        while self._sensor_address != None:
            for device in await BleakScanner.discover():
                if device.name == "temp-sense":
                    self._sensor_address = device.address
                    break

    async def collect_measurements(self, timeout: int):
        async with BleakClient(self._sensor_address) as client:
            if client.is_connected:
                await client.start_notify(_ANALOG_UUID, self._data_callback)
                start_time = time.time()
                while(time.time() - start_time < timeout):
                    await asyncio.sleep(1)