import argparse
import psql_db
from data_graphing import plot_temp_log_func, plot_temps

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--plot_log', action='store_true')
    db = psql_db.Database()
    db.get_params()
    db.connect()
    data_records = db.get_all_data_records()
    for record in data_records:
        print(
            """
            Data ID: {}
            Date Stamp: {}
            Duration (sec): {}
            Average TempF: {}
            Min TempF: {}
            Max TempF: {}
            
            """.format(
                record[0],
                record[1].ctime(),
                record[2],
                record[3],
                record[4],
                record[5]
            )
        )

    data_id = int(input("Enter data_id for desired dataset: "))
    data_record = db.get_single_data_record(data_id)

    args = parser.parse_args()
    setup = db.get_single_setup_record(data_record[4])
    config_id = setup[2]
    config = db.get_single_config_record(config_id)
    db.disconnect()

    if args.plot_log:
        plot_temp_log_func(data=data_record[3], duration_s=data_record[2], sample_period_s=config[5])
    else:
        plot_temps(data=data_record[3], sample_period_s=config[5])