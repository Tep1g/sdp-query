import argparse
import asyncio
import data_processing as dp
import psql_db
from client_bt import ClientBT

_ANALOG_UUID = "000025a8-0000-1000-8000-00805f9b34fb"
_DEVICE_NAME = "temp-sense"

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sampling_duration', type=int, required=True)
    sampling_duration = parser.parse_args().sampling_duration

    db = psql_db.Database
    db.get_params()

    bt = ClientBT(device_name=_DEVICE_NAME, analog_uuid=_ANALOG_UUID)
    await bt.receive_measurements(duration=sampling_duration)

    (a, b, T_amb) = dp.get_decay_params(data=bt.data)

    db.connect()
    db.create_table()
    db.add_record(a=a, b=b, T_amb=T_amb)
    db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())