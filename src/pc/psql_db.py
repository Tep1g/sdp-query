import psycopg2
from datetime import datetime, timezone

class Database:
    def __init__(self):
        self._conn = None
        self._cursor = None
        
    def conect(self, params: dict):
        self._conn = psycopg2.connect(**params)
        self._cursor = self._conn.cursor()

    def create_table(self):
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Temperature (
                data_id SERIAL PRIMARY KEY,
                date_stamp TIMESTAMPTZ,
                a REAL,
                b REAL,
                t_amb REAL
            );
            """
        )

        self._conn.commit()

    # Insert params for equation according to T = a*exp(-b*t) + T_amb
    def add_record(self, a: float, b: float, T_amb: float):
        self._cursor.execute(
            """
            INSERT INTO Temperature (
                data_id,
                date_stamp,
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
                a,
                b,
                T_amb
            )
        )

        self._conn.commit()

    def disconnect(self):
        self._cursor.close()
        self._conn.close()