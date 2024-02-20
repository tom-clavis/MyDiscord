import tkinter as tk

class LoginMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("MyDiscord")
    
        # Définir une police personnalisée
        custom_font = ("Arial", 13)  # Changer "Helvetica" par la police de votre choix

        # Éléments d'interface
        self.label_username = tk.Label(master, text="Nom d'utilisateur")
        self.label_password = tk.Label(master, text="Mot de passe")

        self.entry_username = tk.Entry(master)
        self.entry_password = tk.Entry(master, show="*")  # Pour masquer le mot de passe

        self.button_login = tk.Button(master, text="Se Connecter", command=self.login)
        self.button_register = tk.Button(master, text="S'Inscrire", command=self.register)

        # Centrer les éléments d'interface
        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_login.pack(pady=10)
        self.button_register.pack(pady=10)

        # Ajuster la taille de la fenêtre
        self.master.geometry("600x400")  # Modifiez les dimensions selon vos préférences

    def login(self):
        # Logique de connexion
        username = self.entry_username.get()
        password = self.entry_password.get()
        # Ajoutez ici la logique pour vérifier les informations de connexion dans la base de données

    def register(self):
        # Logique d'inscription
        username = self.entry_username.get()
        password = self.entry_password.get()
        # Ajoutez ici la logique pour enregistrer les nouvelles informations dans la base de données

if __name__ == "__main__":
    root = tk.Tk()
    login_menu = LoginMenu(root)
    # Centrer la fenêtre sur l'écran
    root.eval('tk::PlaceWindow . center')
    root.mainloop()
