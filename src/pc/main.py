import asyncio
from sensor_bt import SensorBT

_ANALOG_UUID = "000025a8-0000-1000-8000-00805f9b34fb"
_DEVICE_NAME = "temp-sense"
_SAMPLING_DURATION = 5

async def main():
    bt = SensorBT(device_name=_DEVICE_NAME, analog_uuid=_ANALOG_UUID)
    await bt.collect_measurements(duration=_SAMPLING_DURATION)

if __name__ == "__main__":
    asyncio.run(main())