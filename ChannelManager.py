import mysql.connector
import os
from ConnectionBD import ConnectionBD
mdp = os.getenv("mdp")

class ChannelManager(ConnectionBD):
    def create_channel(self, name, type):
        self.connect()
        sql = "INSERT INTO channel (name, type) VALUES (%s, %s)"
        val = (name, type)
        self.cursor.execute(sql, val)
        self.connection.commit()
        self.disconnect()

    def read_channel(self):
        self.connect()
        sql = "SELECT * FROM channel "
        self.cursor.execute(sql)
        channel = self.cursor.fetchall()
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
    # Lecture du canal
    channel = channel_manager.read_channel()
    print("Canal trouvé :", channel)


  

 