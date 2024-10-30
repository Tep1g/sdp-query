import psycopg2

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
            CREATE TABLE IF NOT EXISTS Sensor_Data (
                data_id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                sampling_rate REAL,
                measurements INTEGER[]
            );
            """
        )

        self._conn.commit()

    def add_record(self, name: str, sampling_rate: float, measurements: list[int]):

        self._cursor.execute(
            """
            INSERT INTO Sensor_Data (
                data_id,
                name,
                sampling_rate,
                measurements
            )
            VALUES (
                DEFAULT,
                %s,
                %s,
                %s
            );
            """
            ,
            (
                name,
                sampling_rate,
                measurements,
            )
        )

        self._conn.commit()

    def disconnect(self):
        self._cursor.close()
        self._conn.close()