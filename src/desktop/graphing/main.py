import sys
sys.path.append('..')

import argparse
import psql_db
import data_graphing as dg

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--curve_fit_exp_decay', action='store_true')
    db = psql_db.Database()
    db.get_params()
    db.connect()
    data_records = db.get_all_data_descs()
    for record in data_records:
        print(
            """
            Data ID: {}
            Date Stamp: {}
            Duration (sec): {}
            Avg TempF: {:.2f}
            Min TempF: {:.2f}
            Max TempF: {:.2f}
            
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
    db.disconnect()

    if args.curve_fit_exp_decay:
        dg.plot_temp_log_func(data=data_record[3], duration_s=data_record[2])
    else:
        dg.plot_temps(data=data_record[3], duration_s=data_record[2])