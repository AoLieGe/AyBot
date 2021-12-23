class SubApi:
    table_name = "sub"

    @staticmethod
    def create_table():
        return f"""CREATE TABLE IF NOT EXISTS {SubApi.table_name} 
        (
        id              serial PRIMARY KEY,
        twitch_name     varchar(64),
        guild           bigint NOT NULL,
        channel         bigint NOT NULL,
        everyone        boolean,
        status          boolean DEFAULT FALSE,
        offline_count   int DEFAULT 0
        );
        """

    @staticmethod
    def drop_table():
        return f"DROP TABLE IF EXISTS {SubApi.table_name};"

    @staticmethod
    def clear_table():
        return f"DELETE FROM {SubApi.table_name};"

    @staticmethod
    def add_sub(twitch_name, guild, channel, everyone, status, offline_count):
        return f"""INSERT INTO {SubApi.table_name} 
        (twitch_name, guild, channel, everyone, status, offline_count) 
        VALUES ('{twitch_name}', {guild}, {channel}, {everyone}, {status}, {offline_count})
        ;"""

    @staticmethod
    def del_sub(twitch_name, guild):
        return f"""DELETE FROM {SubApi.table_name} WHERE
        twitch_name = '{twitch_name}' AND guild = {guild}
        ;"""

    @staticmethod
    def update_sub(twitch_name, guild, channel, everyone, status, offline_count):
        return f"""UPDATE {SubApi.table_name}
            SET everyone = {everyone}, status = {status}, offline_count = {offline_count}
            WHERE twitch_name = '{twitch_name}' AND guild = {guild} AND channel = {channel}
            ;"""

    @staticmethod
    def get_sub(twitch_name, guild, channel):
        return f"""SELECT * FROM {SubApi.table_name} WHERE
        twitch_name = '{twitch_name}' AND guild = {guild} AND channel = {channel}
        ;"""

    @staticmethod
    def get_subs():
        return f"SELECT * FROM {SubApi.table_name};"
