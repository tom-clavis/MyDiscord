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

    def read_message(self, message_id):
        self.connect()
        sql = "SELECT message.content, message.timestamp, user.first_name, user.last_name FROM message INNER JOIN user ON message.author_id = user.id WHERE message.id = %s"
        self.cursor.execute(sql, (message_id,))
        message = self.cursor.fetchone()
        self.disconnect()
        return message

    def update_message_content(self, message_id, new_content):
        self.connect()
        sql = "UPDATE message SET content = %s WHERE id = %s"
        self.cursor.execute(sql, (new_content, message_id))
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
    # Lecture du message
    message_manager.create_message("test de message", 43, 1 )
    message = message_manager.read_message(18)
    print("Message trouvé :", message)
    message_manager.delete_message(2)
  