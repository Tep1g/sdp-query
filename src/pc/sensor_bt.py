import asyncio
import time
from bleak import BleakScanner, BleakClient

class SensorBT():
    def __init__(self, device_name: str, analog_uuid: str):
        self.data = []
        self._device_name = device_name
        self._analog_uuid = analog_uuid
        self._sensor_address = None

    def _data_callback(self, sender, data):
        self.data.append(int.from_bytes(bytes=data, byteorder='little', signed=False))

    async def connect(self):
        while self._sensor_address != None:
            for device in await BleakScanner.discover():
                if device.name == self._device_name:
                    self._sensor_address = device.address
                    break

    async def collect_measurements(self, timeout: int):
        async with BleakClient(self._sensor_address) as client:
            if client.is_connected:
                await client.start_notify(self._analog_uuid, self._data_callback)
                start_time = time.time()
                while(time.time() - start_time < timeout):
                    await asyncio.sleep(1)