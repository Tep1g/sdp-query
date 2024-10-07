import asyncio
import bluetooth
from bt import BT

# Custom service
SERVICE_UUID = bluetooth.UUID(0x9999)

# org.bluetooth.characteristic.analog
ANALOG_UUID = bluetooth.UUID(0x25A8)

# org.bluetooth.characteristic.gap.appearance.xml
GATT_APPEARANCE_GENERIC_SENSOR = const(1344)

ADV_INTERVAL_US = const(250000)

LED_GPIO = const(16)

async def main():
    bt = BT(
        service_uuid=SERVICE_UUID, 
        char_uuid=ANALOG_UUID, 
        char_appearance=GATT_APPEARANCE_GENERIC_SENSOR, 
        adv_interval=ADV_INTERVAL_US
    )
    bt_task = asyncio.create_task(bt.connect(led_gpio=LED_GPIO))
    await asyncio.gather(bt_task)

if __name__ == "__main__":
    asyncio.run(main())