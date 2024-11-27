import asyncio
from bleak import BleakScanner, BleakClient

class ClientBT():
    def __init__(self, device_name: str, analog_uuid: str):
        self.data = []
        self._device_name = device_name
        self._analog_uuid = analog_uuid

    def _data_callback(self, sender, data):
        self.data.append(int.from_bytes(bytes=data, byteorder='little', signed=False))

    async def receive_measurements(self, duration: int):
        # Get sensor address
        sensor_address = None
        while sensor_address == None:
            for device in await BleakScanner.discover():
                if device.name == self._device_name:
                    sensor_address = device.address

        # Connect and collect measurements
        async with BleakClient(sensor_address) as client:
            if client.is_connected:
                await client.start_notify(char_specifier=self._analog_uuid, callback=self._data_callback)
                await asyncio.sleep(duration)
                await client.stop_notify(char_specifier=self._analog_uuid)