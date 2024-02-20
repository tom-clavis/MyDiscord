import mysql.connector
import os

mdp = os.getenv("mdp")

class Message:
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
    message = message_manager.read_message(2)
    print("Message trouvé :", message)
    message_manager.delete_message(2)
  