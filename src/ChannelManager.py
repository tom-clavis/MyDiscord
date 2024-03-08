import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from ConnectionBD import ConnectionBD
from ChatApp import ChatApp
import bcrypt

mdp = os.getenv("mdp")

class ChannelManager(ConnectionBD):
    def __init__(self, master, user_id, role, host, user, password, database):
        super().__init__(host, user, password, database)
        self.master = master
        self.user_id = user_id
        self.role = role

    def show_channels(self):
        tree = ttk.Treeview(self.master)
        tree["columns"] = ("Id", "Name", "Type", "Channel_type")
        tree["show"] = "headings"
        tree.heading("Id", text="Id")
        tree.heading("Name", text="Nom")
        tree.heading("Type", text="Type")
        tree.heading("Channel_type", text="Channel_type")

        channels = self.read_channel()
        for channel in channels:
            # Ajout de la valeur channel_type
            tree.insert("", "end", values=(channel[0], channel[1], channel[2], channel[3]))  
        tree.pack(expand=True, fill="both")

        tree.bind("<Double-1>", self.open_channel)

        create_channel_button = tk.Button(self.master, text="Créer un canal", command=self.create_channel)
        create_channel_button.pack(pady=10)

    def create_channel(self):
        # Demander à l'utilisateur de saisir toutes les informations nécessaires pour créer un canal
        channel_name = simpledialog.askstring("Créer un canal", "Nom du canal:")
        if not channel_name:
            return  

        channel_type = simpledialog.askstring("Créer un canal", "Type du canal (textuel/vocal):")
        if not channel_type:
            return  

        channel_type = channel_type.lower()
        if channel_type not in ["textuel", "vocal"]:
            messagebox.showerror("Erreur", "Le type de canal doit être 'textuel' ou 'vocal'.")
            return

        channel_visibility = simpledialog.askstring("Créer un canal", "Visibilité du canal (public/private):")
        if not channel_visibility:
            return  

        channel_visibility = channel_visibility.lower()
        if channel_visibility not in ["public", "private"]:
            messagebox.showerror("Erreur", "La visibilité du canal doit être 'public' ou 'privé'.")
            return

        password = None
        if channel_visibility == "private":
            password = simpledialog.askstring("Créer un canal", "Mot de passe du canal (laissez vide pour aucun mot de passe):", show='*')

        # Hash le mot de passe avec Bcrypt 
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        try:
            self.connect()
            sql = "INSERT INTO channel (name, type, channel_type, password) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (channel_name, channel_type, channel_visibility, hashed_password))  # Stockage du mot de passe haché
            self.connection.commit()
            self.disconnect()
            messagebox.showinfo("Succès", f"Canal '{channel_name}' créé avec succès.")
            self.refresh_channels()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du canal : {str(e)}")

    def refresh_channels(self):
        for child in self.master.winfo_children():
            if isinstance(child, ttk.Treeview):
                child.destroy()
        self.show_channels()

    def open_channel(self, event):
        item = event.widget.selection()[0]
        channel_id = event.widget.item(item, "values")[0]
        channel_visibility = event.widget.item(item, "values")[3]
        
        if channel_visibility == "private":
            if self.role == "admin":
                chat_root = tk.Toplevel(self.master)
                chat_app = ChatApp(chat_root, self.user_id, channel_id, role=self.role)
            else:
                password = simpledialog.askstring("Connexion au canal", "Entrez le mot de passe du canal:", show='*')
                if password is None:
                    return  
                # Vérifier si le mot de passe est correct
                if not self.verify_password(channel_id, password):
                    messagebox.showerror("Erreur", "Mot de passe incorrect.")
                    return

        chat_root = tk.Toplevel(self.master)
        chat_app = ChatApp(chat_root, self.user_id, channel_id, role=self.role)

    def verify_password(self, channel_id, password):
        self.connect()
        sql = "SELECT password FROM channel WHERE id = %s"
        self.cursor.execute(sql, (channel_id,))
        correct_password_hash = self.cursor.fetchone()[0]
        self.disconnect()
        
        # Vérifier le mot de passe en comparant le hachage stocké avec le hachage du mot de passe fourni
        return bcrypt.checkpw(password.encode(), correct_password_hash.encode())

    def read_channel(self):
        self.connect()
        sql = "SELECT id, name, type, channel_type FROM channel"
        self.cursor.execute(sql)
        channels = self.cursor.fetchall()
        self.disconnect()
        return channels

if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'

    root = tk.Tk()
    root.title("Channel List")

    channel_manager = ChannelManager(root, user_id=1, role="admin", host=host, user=user, password=password, database=database)
    channel_manager.show_channels()
    root.mainloop()
