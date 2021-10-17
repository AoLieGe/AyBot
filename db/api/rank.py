class RankApi:
    table_name = 'rank'

    @staticmethod
    def create_table():
        return f"""CREATE TABLE IF NOT EXISTS {RankApi.table_name} 
        (
        discord_id  bigint NOT NULL PRIMARY KEY ,
        steam_id    bigint NOT NULL 
        );
        """

    @staticmethod
    def drop_table():
        return f"DROP TABLE IF EXISTS {RankApi.table_name};"

    @staticmethod
    def clear_table():
        return f"DELETE FROM {RankApi.table_name};"

    @staticmethod
    def add_user(discord_id, steam_id):
        return f"""INSERT INTO {RankApi.table_name} 
        (discord_id, steam_id) 
        VALUES ({discord_id}, {steam_id})
        ON CONFLICT (discord_id) DO NOTHING
        ;"""

    @staticmethod
    def del_user(discord_id):
        return f"DELETE FROM {RankApi.table_name} WHERE discord_id = {discord_id};"

    @staticmethod
    def get_user(discord_id):
        return f"SELECT * FROM {RankApi.table_name} WHERE discord_id = {discord_id};"

    @staticmethod
    def get_users():
        return f"SELECT * FROM {RankApi.table_name};"
