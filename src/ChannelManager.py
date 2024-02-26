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

    def add_member_to_channel(self, user_id, channel_id):
        self.connect()
        sql = "INSERT INTO channel_member (user_id, channel_id) VALUES (%s, %s)"
        self.cursor.execute(sql, (user_id, channel_id))
        self.connection.commit()
        self.disconnect()

    def remove_member_from_channel(self, user_id, channel_id):
        self.connect()
        sql = "DELETE FROM channel_member WHERE user_id = %s AND channel_id = %s"
        self.cursor.execute(sql, (user_id, channel_id))
        self.connection.commit()
        self.disconnect()
    
    def read_user_channel(self, user_id):
        self.connect()
        sql = "SELECT user.first_name, user.last_name AS channel_member FROM user LEFT JOIN channel_member ON user.id = channel_member.user_id WHERE channel_member.channel_id = %s;"
        self.cursor.execute(sql, (user_id,))
        user = self.cursor.fetchall()
        self.disconnect()
        if user:
            return user
        else:
            return None

if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'

    channel_manager = ChannelManager(host, user, password, database)
    channel_manager.update_channel_name(3, "General")
    channel = channel_manager.read_channel()
    print("Canal trouvé :", channel)
    read = channel_manager.read_user_channel(1)
    print(read)


 