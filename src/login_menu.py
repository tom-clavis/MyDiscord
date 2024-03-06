import tkinter as tk
from UserManager import UserManager
from RegisterMenu import RegisterMenu
from tkinter import messagebox
import mysql.connector
import os
from ChannelManager import ChannelManager

mdp = os.getenv("mdp")

class LoginMenu():
    def __init__(self, master):
        self.master = master
        self.master.title("MyDiscord")
        self.user_session = None 
        
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
        self.logo_image = tk.PhotoImage(file="Images/logo3.png")
        self.logo_label = tk.Label(self.master, image=self.logo_image, bg="slateblue4")
        self.logo_label.pack(side=tk.BOTTOM, pady=10)
        self.user_manager = UserManager(host="localhost", user="root", password=mdp, database="MyDiscord")
        
    def login(self):
        email = self.entry_usermail.get()
        password = self.entry_password.get()
        try:
            user = self.user_manager.authenticate_user(email, password)

            if user:
                self.user_session = user
                messagebox.showinfo("Succès", "Connexion réussie pour l'email : {}".format(email))
                self.master.destroy()
                # Créez une instance de ChannelManager et appelez sa méthode show_channels()
                root_channel = tk.Tk()
                channel_manager = ChannelManager(root_channel, host="localhost", user="root", password=mdp, database="MyDiscord", user_id=user[0], role=user[5])
                channel_manager.show_channels()

                root_channel.mainloop()
            else:
                messagebox.showerror("Erreur", "Email ou mot de passe invalide")
        except mysql.connector.Error as error:
            print("Erreur lors de la connexion à la base de données:", error)
            
    def check_session(self):
        if self.user_session:
            root_channel = tk.Tk()
            channel_manager = ChannelManager(root_channel, host="localhost", user="root", password=mdp, database="MyDiscord", user_id=self.user_session[0], role=self.user_session[5])
            channel_manager.show_channels()
            root_channel.mainloop()

    def open_register_menu(self):
        register_window = tk.Toplevel(self.master)
        register_menu = RegisterMenu(register_window)
        register_window.eval('tk::PlaceWindow . center')

if __name__ == "__main__":
    root = tk.Tk()
    login_menu = LoginMenu(root)
    login_menu.check_session()
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

