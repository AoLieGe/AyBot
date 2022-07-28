class ClanStatsApi:
    def __init__(self, table_name):
        self.table_name = table_name

    def create_table(self):
        return f"""CREATE TABLE IF NOT EXISTS {self.table_name} 
        (
        steam_id    bigint NOT NULL PRIMARY KEY
        );
        """

    def drop_table(self):
        return f"DROP TABLE IF EXISTS {self.table_name};"

    def clear_table(self):
        return f"DELETE FROM {self.table_name};"

    def add_user(self, steam_id):
        return f"""INSERT INTO {self.table_name} 
        (steam_id) 
        VALUES ({steam_id})
        ON CONFLICT (steam_id) DO NOTHING
        ;"""

    def del_user(self, steam_id):
        return f"DELETE FROM {self.table_name} WHERE steam_id = {steam_id};"

    def get_users(self):
        return f"SELECT * FROM {self.table_name};"
