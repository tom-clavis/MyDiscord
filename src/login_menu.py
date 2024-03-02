import tkinter as tk
from UserManager import UserManager
from RegisterMenu import RegisterMenu
from tkinter import messagebox
import mysql.connector
import os

mdp = os.getenv("mdp")
class LoginMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("MyDiscord")
    
        custom_font = ("Arial Black", 11)

        self.master.config(bg="slateblue4")

        self.label_usermail = tk.Label(master, text="Adresse mail", font=custom_font)
        self.label_password = tk.Label(master, text="Mot de passe", font=custom_font)

        self.entry_usermail = tk.Entry(master, font=custom_font)
        self.entry_password = tk.Entry(master, show="*", font=custom_font)

        self.button_login = tk.Button(master, text="Connexion", command=self.login, font=custom_font)
        self.button_register = tk.Button(master, text="Inscription", command=self.open_register_menu, font=custom_font)

        self.label_usermail.pack(pady=10)
        self.entry_usermail.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_login.pack(pady=10)
        self.button_register.pack(pady=10)

        self.master.geometry("600x450")

        self.logo_image = tk.PhotoImage(file="Images/logo3.png")  # Assurez-vous que l'extension est correcte (par exemple, .png)
        self.logo_label = tk.Label(self.master, image=self.logo_image, bg="slateblue4")  # Changez "lightblue" par la couleur de votre choix
        self.logo_label.pack(side=tk.BOTTOM, pady=10)

        self.user_manager = UserManager(host="localhost", user="root", password=mdp, database="MyDiscord")

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

    def open_register_menu(self):
        register_window = tk.Toplevel(self.master)
        register_menu = RegisterMenu(register_window)
        # Centrer la fenêtre d'inscription sur l'écran
        register_window.eval('tk::PlaceWindow . center')

if __name__ == "__main__":
    root = tk.Tk()
    login_menu = LoginMenu(root)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()