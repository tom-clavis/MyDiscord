import mysql.connector
import os
from ConnectionBD import ConnectionBD

mdp = os.getenv("mdp")

class Message(ConnectionBD):

    def create_message(self, content, author_id, channel_id):
        self.connect()
        sql = "INSERT INTO message (content, author_id, channel_id) VALUES (%s, %s, %s)"
        val = (content, author_id, channel_id)
        self.cursor.execute(sql, val)
        self.connection.commit()
        self.disconnect()

    def delete_message(self, message_id):
        self.connect()
        sql = "DELETE FROM message WHERE id = %s"
        self.cursor.execute(sql, (message_id,))
        self.connection.commit()
        self.disconnect()

if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'

    message_manager = Message(host, user, password, database)
  
  