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

    def create_hw_setup_tables(self):
        table_creation_statements = [
            """
            CREATE TABLE IF NOT EXISTS Thermistor (
                part_number TEXT PRIMARY KEY,
                beta_kΩ INT NOT NULL,
                resistance_Ω_at_25C INT NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Configuration (
                config_id INT PRIMARY KEY,
                is_pull_down_therm BOOLEAN NOT NULL,
                series_resistance_Ω INT NOT NULL,
                adc_bitsize SMALLINT NOT NULL,
                reference_voltage REAL NOT NULL,
                UNIQUE (is_pull_down_therm, series_resistance_Ω, adc_bitsize, reference_voltage)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Setup (
                setup_id INT PRIMARY KEY,
                part_number TEXT NOT NULL,
                config_id INT NOT NULL,
                FOREIGN KEY(part_number) REFERENCES Thermistor (part_number),
                FOREIGN KEY(config_id) REFERENCES Configuration (config_id),
                UNIQUE (part_number, config_id)
            );
            """
        ]
        for statement in table_creation_statements:
            self._cursor.execute(statement)

        self._conn.commit()

    def add_thermistor_record(self, part_number: str, beta: int, resistance_at_25C: int):
        self._cursor.execute(
            """
            INSERT INTO Thermistor (
                part_number,
                beta_kΩ,
                resistance_Ω_at_25C
            )
            VALUES (
                %s,
                %s,
                %s
            );
            """
            ,
            (
                part_number,
                beta,
                resistance_at_25C,
            )
        )

        self._conn.commit()

    def get_all_thermistor_records(self):
        self._cursor.execute(
            """
            SELECT * FROM Thermistor;
            """
        )
        
        return self._cursor.fetchall()

    def get_single_thermistor_record(self, part_number: str):
        try:
            self._cursor.execute(
                """
                SELECT * FROM Thermistor
                WHERE part_number = %s;
                """
                ,
                (part_number,)
            )
        except psycopg2.errors.UndefinedColumn as error:
            if "does not exist" in str(error):
                self._conn.rollback()
                return None
        else:
            return self._cursor.fetchone()

    def add_config_record(
        self,
        config_id: int,
        is_pull_down_therm: bool,
        series_resistance_ohms: int,
        adc_bitsize: int,
        reference_voltage: float,
    ):
        self._cursor.execute(
            """
            INSERT INTO Configuration (
                config_id,
                is_pull_down_therm,
                series_resistance_Ω,
                adc_bitsize,
                reference_voltage
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s
            );
            """
            ,
            (
                config_id,
                is_pull_down_therm,
                series_resistance_ohms,
                adc_bitsize,
                reference_voltage,
            )
        )

        self._conn.commit()

    def get_all_config_records(self):
        self._cursor.execute(
            """
            SELECT * FROM Configuration;
            """
        )

        return self._cursor.fetchall()

    def get_single_config_record(self, config_id: int):
        try:
            self._cursor.execute(
                """
                SELECT * FROM Configuration
                WHERE config_id = %s;
                """
                ,
                (config_id,)
            )
        except psycopg2.errors.UndefinedColumn as error:
            if "does not exist" in str(error):
                self._conn.rollback()
                return None
        else:
            return self._cursor.fetchone()

    def add_setup_record(self, setup_id: int, part_number: str, config_id: int):
        self._cursor.execute(
            """
            INSERT INTO Setup (
                setup_id,
                part_number,
                config_id
            )
            VALUES (
                %s,
                %s,
                %s
            );
            """
            ,
            (
                setup_id,
                part_number,
                config_id,
            )
        )

        self._conn.commit()

    def get_all_setup_records(self):
        self._cursor.execute(
            """
            SELECT * FROM Setup;
            """
        )

        return self._cursor.fetchall()

    def get_single_setup_record(self, setup_id: int):
        try:
            self._cursor.execute(
                """
                SELECT * FROM Setup
                WHERE setup_id = %s;
                """
                ,
                (setup_id,)
            )
        except psycopg2.errors.UndefinedColumn as error:
            if "does not exist" in str(error):
                self._conn.rollback()
                return None
        else:
            return self._cursor.fetchone()

    def create_data_table(self):
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Temperature (
                data_id SERIAL PRIMARY KEY,
                date_stamp TIMESTAMPTZ,
                duration INT,
                degF_points REAL[],
                setup_id INT NOT NULL,
                FOREIGN KEY(setup_id) REFERENCES Setup (setup_id)
            );
            """
        )

        self._conn.commit()

    def add_data_record(self, duration: int, degF_points: list[float], setup_id: int):
        self._cursor.execute(
            """
            INSERT INTO Temperature (
                data_id,
                date_stamp,
                duration,
                degF_points,
                setup_id
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
                degF_points,
                setup_id
            )
        )

        self._conn.commit()

    def get_all_data_records(self):
        self._cursor.execute(
            """
            SELECT 
                data_id,
                date_stamp,
                duration,
                AVG(data) as average_tempF,
                MIN(data) as min_tempF,
                MAX(data) as max_tempF
            FROM (
                SELECT data_id, date_stamp, duration, UNNEST(degF_points) as data
                FROM Temperature
            ) subquery
            GROUP BY data_id, date_stamp, duration
            ORDER BY data_id, date_stamp, duration;
            """
        )
        return self._cursor.fetchall()
    
    def get_single_data_record(self, data_id: int) -> tuple[int, list[float]]:
        try:
            self._cursor.execute(
                """
                SELECT * FROM Temperature
                WHERE data_id = %s;
                """
                ,
                (data_id,)
            )
        except psycopg2.errors.UndefinedColumn as error:
            if "does not exist" in str(error):
                self._conn.rollback()
                return None
        else:
            return self._cursor.fetchone()

    def disconnect(self):
        self._cursor.close()
        self._conn.close()