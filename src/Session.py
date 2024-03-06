import mysql.connector
import os

mdp = os.getenv("mdp")

class Session:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        # Vous pouvez stocker d'autres informations de session ici

class LoginMenu:
    def login(self):
        # Logique de connexion
        email = self.entry_usermail.get()
        password = self.entry_password.get()
        
        try:
            # Connexion à la base de données
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=mdp,
                database="MyDiscord"
            )
            
            cursor = connection.cursor()

            # Authentifier l'utilisateur
            user = self.user_manager.authenticate_user(email, password)

            if user:
                # Si l'utilisateur est authentifié avec succès
                connection.commit()
                print("Bienvenue:", email)
                messagebox.showinfo("Succès", "Connexion réussie pour l'email : {}".format(email))
                # Créer une session
                self.session = Session(user["user_id"], email)
                self.master.destroy()  # Ferme la fenêtre d'inscription
            else:
                # Si l'utilisateur n'est pas authentifié
                messagebox.showerror("Erreur", "Email ou mot de passe invalide")

        except mysql.connector.Error as error:
            # Gestion des erreurs liées à la base de données
            print("Erreur lors de la connexion à la base de données:", error)

        finally:
            # Fermez la connexion
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()