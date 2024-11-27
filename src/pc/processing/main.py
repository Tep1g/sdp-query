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

    db = psql_db.Database()
    db.get_params()
    db.connect()
    db.create_hw_setup_tables()
    db.create_data_table()

    # Get setup information
    setups = db.get_all_setup_records()
    if setups == None:
        print("No setups found, creating one")
        add_new_setup = True
    else:
        add_new_setup = False
        for setup in setups:
            therm = db.get_single_thermistor_record(setup[1])
            config = db.get_single_config_record(setup[2])
            print(
                """
                Setup ID: {}
                ------------
                Thermistor Specs
                Model Number: {}
                Beta Value (kΩ): {}
                Resistance (Ω) at 25C: {}
                ------------
                Configuration
                Is Pull-Down: {}
                Series Resistance (Ω): {}
                """.format(
                    setup[0],
                    therm[0],
                    therm[1],
                    therm[2],
                    config[0],
                    config[1]
                )
            )

    if add_new_setup or input("Choose pre-existing setup?: ").lower()=="no":
        # Add thermistor
        therm_records = db.get_all_thermistor_records()
        if therm_records == None:
            add_new_therm = True
        else:
            add_new_therm = False
            for record in therm_records:
                print(
                    """
                    Model Number: {}
                    Beta Value: {}
                    Resistance (Ω) at 25C: {}
                    """.format(record[0], record[1], record[2])
                )

        if (add_new_therm) or (input("Choose existing thermistor?: ").lower() == "no"):
            print("Adding new thermistor record to database")
            part_number = input("Enter part number: ")
            therm_specs_obtained = False
            therm = db.get_single_thermistor_record(part_number)
            if therm != None:
                print("Part already exists, retrieving part specs for {}".format(part_number))
                beta = therm[1]
                res_at_25C = therm[2]
                therm_specs_obtained = True

            if not therm_specs_obtained:
                beta = int(input("Enter beta value (KΩ): "))
                res_at_25C = int(input("Enter resistance at 25C (Ω)"))
                db.add_thermistor_record(part_number, beta, res_at_25C)
        else:
            part_number = input("Enter part number: ")
            therm = db.get_single_thermistor_record(part_number)
            beta = therm[1]
            res_at_25C = therm[2]

        # Add configuration
        config_records = db.get_all_config_records()
        if config_records == None:
            print("No configurations found")
            add_new_config = True
        else:
            add_new_config = False
            for record in config_records:
                print(
                    """
                    Config ID: {}
                    Is Pull-Down: {}
                    Series Resistance (Ω): {}
                    """.format(record[0], record[1], record[2])
                )

        if (add_new_config) or (input("Choose existing configuration?: ").lower() == "no"):
            print("Adding new configuration record to database")
            is_pull_down = True if input("Thermistor is pull-down?: ").lower()=="yes" else False
            series_resistance = int(input("Enter series resistance (Ω): "))
            db.add_config_record(is_pull_down, series_resistance)
            config = db.get_single_config_record(is_pull_down_therm=is_pull_down, series_resistance=series_resistance)
            config_id = config[0]
        else:
            config_id = input("Enter config id: ")
            config = db.get_single_config_record(config_id=config_id)
            is_pull_down = config[1]
            series_resistance = config[2]

        db.add_setup_record(part_number=part_number, config_id=config_id)
        setup = db.get_single_setup_record(part_number=part_number, config_id=config_id)
        setup_id = setup[0]

    else:
        # Get setup_id
        setup_id = int(input("Enter desired setup id: "))
        setup = db.get_single_setup_record(setup_id=setup_id)
        config = db.get_single_config_record(config_id=setup[2])
        therm = db.get_single_thermistor_record(part_number=setup[1])

        # Get thermistor and configuration information
        setup_id = setup[0]
        beta = therm[1]
        res_at_25C = therm[2]
        is_pull_down = config[1]
        res_at_25C = config[2]

    bt = ClientBT(device_name=_DEVICE_NAME, analog_uuid=_ANALOG_UUID)
    await bt.receive_measurements(duration=sampling_duration)

    db.add_data_record(duration=sampling_duration, degF_points=bt.data, setup_id=setup_id)
    db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())