import tkinter as tk
from tkinter import messagebox
from UserManager import UserManager
import mysql.connector
import os

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

        self.master.geometry("400x450")
        
        self.user_manager = UserManager(host="localhost", user="root", password=mdp, database="MyDiscord")

    def register(self):
        name = self.entry_name.get()
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        try:
            self.user_manager.create_user(name, username, email, password)
            messagebox.showinfo("Succès", "Inscription réussie pour l'utilisateur: {}\navec l'adresse e-mail: {}".format(username, email))
            self.clear_entries()
            self.master.destroy()  # Ferme la fenêtre d'inscription
        
        except mysql.connector.Error as error:
            print("Erreur lors de l'insertion dans la base de données:", error)
            messagebox.showerror("Erreur", "Une erreur est survenue lors de l'inscription.")

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_username.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    register_menu = RegisterMenu(root)
    root.mainloop()

