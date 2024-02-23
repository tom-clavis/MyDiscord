import tkinter as tk

from RegisterMenu import RegisterMenu


class LoginMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("MyDiscord")
    
        custom_font = ("Arial Black", 11)

        self.master.config(bg="slateblue4")

        self.label_username = tk.Label(master, text="Nom d'utilisateur", font=custom_font)
        self.label_password = tk.Label(master, text="Mot de passe", font=custom_font)

        self.entry_username = tk.Entry(master, font=custom_font)
        self.entry_password = tk.Entry(master, show="*", font=custom_font)

        self.button_login = tk.Button(master, text="Connexion", command=self.login, font=custom_font)
        self.button_register = tk.Button(master, text="Inscription", command=self.open_register_menu, font=custom_font)

        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_login.pack(pady=10)
        self.button_register.pack(pady=10)

        self.master.geometry("600x450")

    def login(self):
        # Logique de connexion
        username = self.entry_username.get()
        password = self.entry_password.get()
        # Ajoutez ici la logique pour vérifier les informations de connexion dans la base de données

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
