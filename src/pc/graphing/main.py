import psql_db
from data_graphing import plot_temp_func

if __name__ == "__main__":
    db = psql_db.Database()
    db.get_params()
    db.connect()
    records = db.get_all_records()
    for record in records:
        print(record)

    db.disconnect()

    data_id = int(input("Enter data_id for desired dataset: "))
    for record in records:
        if record[0] == data_id:
            duration = record[2]
            a = record[3]
            b = record[4]
            T_amb = record[5]

    plot_temp_func(duration_s=duration, a=a, b=b, T_amb=T_amb)