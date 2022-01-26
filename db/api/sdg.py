class SdgApi:
    table_name = 'sdg'

    @staticmethod
    def create_table():
        return f"""CREATE TABLE IF NOT EXISTS {SdgApi.table_name} 
        (
        steam_id    bigint NOT NULL PRIMARY KEY,
        rate        int NOT NULL,
        delta       int,
        time        bigint
        );
        """

    @staticmethod
    def drop_table():
        return f"DROP TABLE IF EXISTS {SdgApi.table_name};"

    @staticmethod
    def clear_table():
        return f"DELETE FROM {SdgApi.table_name};"

    @staticmethod
    def add_user(steam_id, rate, delta, time):
        return f"""INSERT INTO {SdgApi.table_name} 
        (steam_id, rate, delta, time) 
        VALUES ({steam_id}, {rate}, {delta}, {time})
        ON CONFLICT (steam_id) DO NOTHING
        ;"""

    @staticmethod
    def update_user(steam_id, rate, delta, time):
        return f"""UPDATE {SdgApi.table_name}
                SET rate = {rate}, delta = {delta}, time = {time}
                WHERE steam_id = '{steam_id}'
                ;"""

    @staticmethod
    def del_user(steam_id):
        return f"DELETE FROM {SdgApi.table_name} WHERE steam_id = {steam_id};"

    @staticmethod
    def get_user(steam_id):
        return f"SELECT * FROM {SdgApi.table_name} WHERE steam_id = {steam_id};"

    @staticmethod
    def get_users():
        return f"SELECT * FROM {SdgApi.table_name};"
