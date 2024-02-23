import tkinter as tk
from tkinter import messagebox

class RegisterMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Inscription")
        self.master.config(bg="slateblue4")

        custom_font = ("Arial Black", 11)

        self.label_username = tk.Label(master, text="Nom d'utilisateur", font=custom_font)
        self.label_email = tk.Label(master, text="Adresse e-mail", font=custom_font)
        self.label_password = tk.Label(master, text="Mot de passe", font=custom_font)

        self.entry_username = tk.Entry(master, font=custom_font)
        self.entry_email = tk.Entry(master, font=custom_font)
        self.entry_password = tk.Entry(master, show="*", font=custom_font)

        self.button_register = tk.Button(master, text="Inscription", command=self.register, font=custom_font)

        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_email.pack(pady=10)
        self.entry_email.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.button_register.pack(pady=10)

        self.master.geometry("400x350")

    def register(self):
        
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        
        print("Inscription réussie pour l'utilisateur:", username, "avec l'adresse e-mail:", email)
        messagebox.showinfo("Succès", "Inscription réussie pour l'utilisateur: {}\navec l'adresse e-mail: {}".format(username, email))
        self.master.destroy()  # Ferme la fenêtre d'inscription

if __name__ == "__main__":
    root = tk.Tk()
    register_menu = RegisterMenu(root)
    root.mainloop()
