import argparse
import asyncio
from client_bt import ClientBT

_ANALOG_UUID = "000025a8-0000-1000-8000-00805f9b34fb"
_DEVICE_NAME = "temp-sense"

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sampling_duration', type=int, required=True)
    sampling_duration = parser.parse_args().sampling_duration

    bt = ClientBT(device_name=_DEVICE_NAME, analog_uuid=_ANALOG_UUID)
    await bt.receive_measurements(duration=sampling_duration)

if __name__ == "__main__":
    asyncio.run(main())