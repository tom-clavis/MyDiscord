import mysql.connector
import os

mdp = os.getenv("mdp")

class User:
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

    def create_user(self, first_name, last_name, email, password, id_user):
        # Vérifier si l'utilisateur existe déjà avec cet e-mail
        existing_user = self.read_user(email)
        if existing_user:
            print("L'utilisateur avec cet e-mail existe déjà.")
            return
        self.connect()
        sql = "INSERT INTO user (first_name, last_name, email, password, id_user) VALUES (%s, %s, %s, %s, %s)" 
        val = (first_name, last_name, email, password, id_user)
        self.cursor.execute(sql, val)
        self.connection.commit()
        self.disconnect()

    def read_user(self, email):
        self.connect()
        sql = "SELECT * FROM user WHERE email = %s"
        self.cursor.execute(sql, (email,))
        user = self.cursor.fetchone()
        self.disconnect()
        return user

    def update_user_password(self, new_mail, new_password, email):
        self.connect()
        sql = "UPDATE user SET email = %s, password = %s WHERE email = %s"
        self.cursor.execute(sql, (new_mail, new_password, email))
        self.connection.commit()
        self.disconnect()

    def delete_user_by_email(self, email):
        self.connect()
        sql = "DELETE FROM user WHERE email = %s"
        self.cursor.execute(sql, (email,))
        self.connection.commit()
        self.disconnect()


if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'

    user_manager = User(host, user, password, database)

    # création user
    user_manager.create_user("John", "Doe", "john@example.com", "test", 1)
    user_manager.update_user_password("test@example.com", "123", "john@example.com" )
    # voir les données de l'user
    user = user_manager.read_user("test@example.com")
    print("Utilisateur trouvé :", user) 
    
    

    
