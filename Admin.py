import mysql.connector

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

    def delete_user_by_email(self, email):
            self.connect()
            sql = "DELETE FROM user WHERE email = %s"
            self.cursor.execute(sql, (email,))
            self.connection.commit()
            self.disconnect()