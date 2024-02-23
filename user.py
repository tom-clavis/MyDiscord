import os
from UserManager import UserManager

mdp = os.getenv("mdp")

class User:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    def send_message(self, email, password, content):
        authenticated_user = self.user_manager.authenticate_user(email, password)
        if authenticated_user:
            user_id = authenticated_user[0]  # Récupérer l'ID de l'utilisateur authentifié
            self.user_manager.connect()
            sql = "INSERT INTO message (content, author_id) VALUES (%s, %s)"
            val = (content, user_id)
            self.user_manager.cursor.execute(sql, val)
            self.user_manager.connection.commit()
            self.user_manager.disconnect()
            print("Message envoyé avec succès.")
        else:
            print("Impossible d'envoyer le message. Authentification invalide.")
            
    def create_user(self, email, password):
        if not self.user_manager.user_exists(email):
            self.user_manager.connect()
            sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
            val = (email, password)
            self.user_manager.cursor.execute(sql, val)
            self.user_manager.connection.commit()
            self.user_manager.disconnect()
            print("Utilisateur créé avec succès.")
        else:
            print("L'utilisateur existe déjà.")


if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'
    
    user_manager = UserManager(host, user, password, database)  

    # Authentification de l'utilisateur
    email = "bobo@example.com"
    password = "111"
    
    authenticated_user = user_manager.authenticate_user(email, password)
    if authenticated_user:
        print("Connexion réussie pour l'utilisateur :", authenticated_user)
    else:
        print("Email ou mot de passe incorrect.")

    user_instance = User(user_manager)
    user_instance.send_message("bobo@example.com", "111", "hahahaha")
