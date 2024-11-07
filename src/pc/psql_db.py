import psycopg2
from datetime import datetime, timezone

class Database:
    def __init__(self):
        self._conn = None
        self._cursor = None
        self._params = {}
        
    def get_params(self) -> dict:
        password = input("Enter password: ")

        params = []
        with open("params.txt", "r") as file:
            for line in file:
                params.append(line.strip())

        self._params = {
            "dbname"    : params[0],
            "host"      : params[1],
            "user"      : params[2],
            "password"  : password,
            "port"      : params[3],
            "sslmode"   : params[4]
        }

    def connect(self):
        self._conn = psycopg2.connect(**self._params)
        self._cursor = self._conn.cursor()

    def create_table(self):
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Temperature (
                data_id SERIAL PRIMARY KEY,
                date_stamp TIMESTAMPTZ,
                duration INT,
                a REAL,
                b REAL,
                t_amb REAL
            );
            """
        )

        self._conn.commit()

    # Insert params for equation according to T = a*exp(-b*t) + T_amb
    def add_record(self, duration: int, a: float, b: float, T_amb: float):
        self._cursor.execute(
            """
            INSERT INTO Temperature (
                data_id,
                date_stamp,
                duration,
                a,
                b,
                t_amb
            )
            VALUES (
                DEFAULT,
                %s,
                %s,
                %s,
                %s
            );
            """
            ,
            (
                datetime.now(timezone.utc),
                duration,
                a,
                b,
                T_amb
            )
        )

        self._conn.commit()

    def get_all_records(self):
        self._cursor.execute(
            """
            SELECT * FROM Temperature;
            """
        )
        return self._cursor.fetchall()

    def disconnect(self):
        self._cursor.close()
        self._conn.close()