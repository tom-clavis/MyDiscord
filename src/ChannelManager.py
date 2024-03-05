import tkinter as tk
from tkinter import ttk
import os
from ConnectionBD import ConnectionBD
from ChatApp import ChatApp

mdp = os.getenv("mdp")

class ChannelManager(ConnectionBD):
    def __init__(self, master, user_id, host, user, password, database):
        super().__init__(host, user, password, database)
        self.master = master
        self.user_id = user_id

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
            tree.insert("", "end", values=(channel[1], channel[2], channel[3]))
        tree.pack(expand=True, fill="both")

    def read_channel(self):
        self.connect()
        sql = "SELECT * FROM channel "
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


    


 