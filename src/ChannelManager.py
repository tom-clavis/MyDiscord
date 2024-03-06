import tkinter as tk
from tkinter import ttk
import os
from ConnectionBD import ConnectionBD
from ChatApp import ChatApp

mdp = os.getenv("mdp")

class ChannelManager(ConnectionBD):
    def __init__(self, master, user_id, role, host, user, password, database):
        super().__init__(host, user, password, database)
        self.master = master
        self.user_id = user_id
        self.role = role
        print("le role est", self.role)

    def show_channels(self):
        # Utilisez self.master pour référencer la fenêtre principale
        tree = ttk.Treeview(self.master)
        tree["columns"] = ("Name", "Type", "Channel_type")
        tree["show"] = "headings"
        tree.heading("Name", text="Nom")
        tree.heading("Type", text="Type")
        tree.heading("Channel_type", text="Channel_type")

        # Lire les canaux depuis la base de données
        channels = self.read_channel()
        for channel in channels:
            tree.insert("", "end", values=(channel[0], channel[1], channel[2]))
        tree.pack(expand=True, fill="both")

        # Lorsque l'utilisateur sélectionne un canal, affichez les messages et les utilisateurs correspondants
        tree.bind("<Double-1>", self.open_channel)

    def open_channel(self, event):
        item = event.widget.selection()[0]  # Obtenir l'élément sélectionné dans l'arbre
        channel_id = event.widget.item(item, "values")[0]  # Obtenir l'ID du canal sélectionné
        # Afficher l'application de chat pour le canal sélectionné
        chat_root = tk.Toplevel(self.master)
        chat_app = ChatApp(chat_root, self.user_id, channel_id, role=self.role)

    def read_channel(self):
        self.connect()
        sql = "SELECT id, name, type FROM channel "  
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

    channel_manager = ChannelManager(root, user_id=1, host=host, user=user, password=password, database=database)
    channel_manager.show_channels()

    root.mainloop()
    


 