import mysql.connector
import bcrypt
class Connection:
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


    def authenticate_user(self, email, password):
        user = self.read_user(email)
        if user:
            hashed_password = user[4]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return user
        return None