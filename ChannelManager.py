import mysql.connector
import os

mdp = os.getenv("mdp")

class ChannelManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def create_channel(self, name):
        self.connect()
        sql = "INSERT INTO channel (name) VALUES (%s)"
        val = (name,)
        self.cursor.execute(sql, val)
        self.connection.commit()
        self.disconnect()

    def read_channel(self, channel_id):
        self.connect()
        sql = "SELECT * FROM channel WHERE id = %s"
        self.cursor.execute(sql, (channel_id,))
        channel = self.cursor.fetchone()
        self.disconnect()
        return channel

    def update_channel_name(self, channel_id, new_name):
        self.connect()
        sql = "UPDATE channel SET name = %s WHERE id = %s"
        self.cursor.execute(sql, (new_name, channel_id))
        self.connection.commit()
        self.disconnect()

    def delete_channel(self, channel_id):
        self.connect()
        sql = "DELETE FROM channel WHERE id = %s"
        self.cursor.execute(sql, (channel_id,))
        self.connection.commit()
        self.disconnect()

if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'

    channel_manager = ChannelManager(host, user, password, database)

    # Création d'un canal
    channel_manager.create_channel("general")

    # Lecture du canal
    channel = channel_manager.read_channel(1)
    print("Canal trouvé :", channel)

    # Mise à jour du nom du canal
    channel_manager.update_channel_name(1, "general-discussion")

    # Suppression du canal
    channel_manager.delete_channel(1)