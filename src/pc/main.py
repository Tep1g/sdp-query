from sensor_bt import SensorBT

_ANALOG_UUID = const("000025a8-0000-1000-8000-00805f9b34fb")
_DEVICE_NAME = const("temp-sense")
_SAMPLING_DURATION = const(1200)

if __name__ == "__main__":
    bt = SensorBT(device_name=_DEVICE_NAME, analog_uuid=_ANALOG_UUID)
    bt.collect_measurements(duration=_SAMPLING_DURATION)