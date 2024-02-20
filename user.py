import mysql.connector
import os
import bcrypt
from Connection import Connection
mdp = os.getenv("mdp")

class User(Connection):

    def disconnect(self):
        self.connection.close()

    def create_user(self, first_name, last_name, email, password, id_user):
        existing_user = self.read_user(email)
        if existing_user:
            return
        self.connect()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO user (first_name, last_name, email, password, id_user) VALUES (%s, %s, %s, %s, %s)"
        val = (first_name, last_name, email, hashed_password, id_user)
        self.cursor.execute(sql, val)
        self.connection.commit()
        self.disconnect()

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
   
    def update_user_password(self, new_mail, new_password, email):
        self.connect()
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        sql = "UPDATE user SET email = %s, password = %s WHERE email = %s"
        self.cursor.execute(sql, (new_mail, hashed_password, email))
        self.connection.commit()
        self.disconnect()

    def send_message(self, email, password, content):
        authenticated_user = self.authenticate_user(email, password)
        if authenticated_user:
            user_id = authenticated_user[0]  # Récupérer l'ID de l'utilisateur authentifié
            self.connect()
            sql = "INSERT INTO message (content, author_id) VALUES (%s, %s)"
            val = (content, user_id)
            self.cursor.execute(sql, val)
            self.connection.commit()
            self.disconnect()
            print("Message envoyé avec succès.")
        else:
            print("Impossible d'envoyer le message. Authentification invalide.")


if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'

    user_manager = User(host, user, password, database)  
    user_manager.create_user("john", "doe", "john@example.com", "456", 1)
    # Authentification de l'utilisateur
    email = "john@example.com"
    password = "456"
    authenticated_user = user_manager.authenticate_user(email, password)
    if authenticated_user:
        print("Connexion réussie pour l'utilisateur :", authenticated_user)
    else:
        print("Email ou mot de passe incorrect.")

    user_manager.send_message("john@example.com","456","teeeeeeeeeeeeeeest")


    
    

    
