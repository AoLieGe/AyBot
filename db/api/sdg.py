class SdgApi:
    table_name = 'sdg'

    @staticmethod
    def create_table():
        return f"""CREATE TABLE IF NOT EXISTS {SdgApi.table_name} 
        (
        steam_id    bigint NOT NULL PRIMARY KEY
        );
        """

    @staticmethod
    def drop_table():
        return f"DROP TABLE IF EXISTS {SdgApi.table_name};"

    @staticmethod
    def clear_table():
        return f"DELETE FROM {SdgApi.table_name};"

    @staticmethod
    def add_user(steam_id):
        return f"""INSERT INTO {SdgApi.table_name} 
        (steam_id) 
        VALUES ({steam_id})
        ON CONFLICT (steam_id) DO NOTHING
        ;"""

    @staticmethod
    def del_user(steam_id):
        return f"DELETE FROM {SdgApi.table_name} WHERE steam_id = {steam_id};"

    @staticmethod
    def get_users():
        return f"SELECT * FROM {SdgApi.table_name};"
