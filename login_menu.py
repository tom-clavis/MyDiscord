import tkinter as tk

class LoginMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("MyDiscord")
    
        # Définir une police
        custom_font = ("Arial Black", 11)

        # Changer la couleur de fond de la fenêtre
        self.master.config(bg="slateblue4")  # Changez "lightblue" par la couleur de votre choix


        # Éléments d'interface avec la police personnalisée
        self.label_username = tk.Label(master, text="Nom d'utilisateur", font=custom_font)
        self.label_password = tk.Label(master, text="Mot de passe", font=custom_font)

        self.entry_username = tk.Entry(master, font=custom_font)
        self.entry_password = tk.Entry(master, show="*", font=custom_font)  # Pour masquer le mot de passe

        self.button_login = tk.Button(master, text="Connexion", command=self.login, font=custom_font)
        self.button_register = tk.Button(master, text="Inscription", command=self.register, font=custom_font)

        # Centrer les éléments d'interface
        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_login.pack(pady=10)
        self.button_register.pack(pady=10)

         # Ajouter le logo en bas de la page
        self.logo_image = tk.PhotoImage(file="logo3.png")  
        self.logo_label = tk.Label(self.master, image=self.logo_image, bg="slateblue4") 
        self.logo_label.pack(side=tk.BOTTOM, pady=10)

        # Ajuster la taille de la fenêtre
        self.master.geometry("600x450") 

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
