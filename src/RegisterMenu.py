import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
import bcrypt  # Importez bcrypt pour utiliser ses fonctions de hachage
from UserManager import UserManager


mdp = os.getenv("mdp")

class RegisterMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Inscription")
        self.master.config(bg="slateblue4")

        custom_font = ("Arial Black", 11)

        self.label_name = tk.Label(master, text="Nom", font=custom_font)
        self.label_username = tk.Label(master, text="Prénom", font=custom_font)
        self.label_email = tk.Label(master, text="Adresse e-mail", font=custom_font)
        self.label_password = tk.Label(master, text="Mot de passe", font=custom_font)

        self.entry_name = tk.Entry(master, font=custom_font)
        self.entry_username = tk.Entry(master, font=custom_font)
        self.entry_email = tk.Entry(master, font=custom_font)
        self.entry_password = tk.Entry(master, show="*", font=custom_font)

        self.button_register = tk.Button(master, text="Inscription", command=self.register, font=custom_font)

        self.label_name.pack(pady=10)
        self.entry_name.pack(pady=10)
        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_email.pack(pady=10)
        self.entry_email.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_register.pack(pady=10)

        self.master.geometry("400x350")
        
        # Instanciez UserManager
        self.user_manager = UserManager(host="localhost", user="root", password=mdp, database="MyDiscord")

    def register(self):
        name = self.entry_name.get()
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        connection = None  # Initialize connection variable
        
        try:
            # Connexion à la base de données
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=mdp ,
                database="MyDiscord"
            )
            
            cursor = connection.cursor()

            # Appelez la méthode create_user de UserManager
            self.user_manager.create_user(name, username, email, password)
            
            # Fermez la connexion
            connection.commit()
            print("Inscription réussie pour l'utilisateur:", username, "avec l'adresse e-mail:", email)
            messagebox.showinfo("Succès", "Inscription réussie pour l'utilisateur: {}\navec l'adresse e-mail: {}".format(username, email))
            self.master.destroy()  # Ferme la fenêtre d'inscription
        
        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion dans la base de données:", error)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de l'inscription.")
        
        finally:
            # Fermez la connexion
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    register_menu = RegisterMenu(root)
    root.mainloop()
