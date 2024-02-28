import mysql.connector
import os
import bcrypt
from ConnectionBD import ConnectionBD

mdp = os.getenv("mdp")

class UserManager(ConnectionBD):
    def read_user(self, email):
        self.connect()
        sql = "SELECT * FROM user WHERE email = %s"
        self.cursor.execute(sql, (email,))
        user = self.cursor.fetchone()
        self.disconnect()
        if user:
            return user
        else:
            return None
        
    def authenticate_user(self, email, password):
        user = self.read_user(email)
        if user:
            hashed_password = user[4]
            
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return user
        return None
        
        
    def connect(self):
        # Establish connection to the database
        self.connection = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cursor = self.connection.cursor()

    def register_user(self, username, email, password):
        # Insert user information into the database
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        val = (username, email, password)
        self.cursor.execute(sql, val)
        self.connection.commit()
        
if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'
    user_manager = UserManager(host, user, password, database)
    user = user_manager.read_user("john@example.com")