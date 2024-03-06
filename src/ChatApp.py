import tkinter as tk
from tkinter import scrolledtext
import os
from tkinter import Button
from Message import Message

class ChatApp:
    def __init__(self, master, user_id, channel_id, role):
        self.master = master
        self.user_id = user_id  # ID de l'utilisateur connecté
        self.channel_id = channel_id  # ID du canal auquel l'utilisateur est connecté
        self.role = role
        print (self.role)
        self.master.title("Discord-like Chat")
        self.master.geometry("600x400")

        # Connexion à la base de données
        host = 'localhost'
        user = 'root'
        password = os.getenv("mdp")
        database = 'MyDiscord'
        self.message_manager = Message(host, user, password, database)

        # Ajouter l'utilisateur au canal
        self.add_user_to_channel()

        # Liste statique de messages
        self.messages = self.load_messages()  # Charge les messages depuis la base de données

        # Zone de texte déroulante pour afficher les messages
        self.message_list = scrolledtext.ScrolledText(master, wrap=tk.WORD, state=tk.DISABLED)
        self.message_list.pack(expand=True, fill="both")

        # Zone de texte déroulante pour afficher les utilisateurs sur le canal
        self.user_list = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state=tk.DISABLED, width=40, height=10)
        self.user_list.pack(expand=True, fill="both")

        # Entrée pour taper un nouveau message
        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(pady=10)

        # Bouton pour envoyer un message
        send_button = tk.Button(master, text="Send", command=self.send_message)
        send_button.pack()

        # Afficher les messages initiaux
        self.display_messages()


        # Initialisation de la liste des boutons de suppression des utilisateurs
        self.delete_user_buttons = []

        # Affichage des utilisateurs avec leurs boutons de suppression
        self.display_users()
        
    def get_author_name(self, author_id):
        self.message_manager.connect()
        sql = "SELECT first_name FROM user WHERE id = %s"
        self.message_manager.cursor.execute(sql, (author_id,))
        row = self.message_manager.cursor.fetchone()
        author_name = row[0] if row else None
        self.message_manager.disconnect()
        return author_name

    def add_user_to_channel(self):
        # Connexion à la base de données
        self.message_manager.connect()
        # Insérer l'utilisateur dans la table channel_member
        sql = "INSERT INTO channel_member (user_id, channel_id) VALUES (%s, %s)"
        self.message_manager.cursor.execute(sql, (self.user_id, self.channel_id))
        # Valider et enregistrer les modifications
        self.message_manager.connection.commit()
        # Déconnexion de la base de données
        self.message_manager.disconnect()

    def get_users_in_channel(self):
        self.message_manager.connect()
        sql = "SELECT DISTINCT user_id FROM channel_member WHERE channel_id = %s"
        self.message_manager.cursor.execute(sql, (self.channel_id,))
        rows = self.message_manager.cursor.fetchall()
        user_ids = [row[0] for row in rows]
        self.message_manager.disconnect()
        return user_ids

    def display_users(self):
        users = self.get_users_in_channel()
        self.user_list.config(state=tk.NORMAL)
        self.user_list.delete(1.0, tk.END)  # Effacer le contenu actuel

        for name in users:
            user_name = self.get_author_name(name)
            user_frame = tk.Frame(self.master)
            user_frame.pack()
            
            label_id = tk.Label(user_frame, text=f"Nom: {name}")
            label_id.pack(side=tk.LEFT)
            

            # Condition pour afficher le bouton de suppression uniquement si l'utilisateur est un administrateur
            if self.role == 'admin':
                # Passer l'identifiant de l'utilisateur à supprimer à la fonction delete_user
                delete_button = Button(user_frame, text="Supprimer", command=lambda user_id=name: self.delete_user(user_id))
                delete_button.pack(side=tk.RIGHT)
                self.delete_user_buttons.append(delete_button)

        self.user_list.config(state=tk.DISABLED)



    def delete_user(self, user_id):
        # Connexion à la base de données
        self.message_manager.connect()
        # Supprimer l'utilisateur du canal dans la base de données
        sql = "DELETE FROM channel_member WHERE channel_id = %s AND user_id = %s"
        print("supprimé : ", user_id)
        self.message_manager.cursor.execute(sql, (self.channel_id, user_id))
        # Valider et enregistrer les modifications
        self.message_manager.connection.commit()
        # Déconnexion de la base de données
        self.message_manager.disconnect()
        # Actualiser l'affichage des utilisateurs
        self.display_users()



    def load_messages(self):
        messages = []
        self.message_manager.connect()
        sql = "SELECT content, timestamp, author_id FROM message WHERE channel_id = %s ORDER BY timestamp"
        self.message_manager.cursor.execute(sql, (self.channel_id,))
        rows = self.message_manager.cursor.fetchall()

        for row in rows:
            # Récupérer le nom de l'utilisateur à partir de l'ID de l'auteur
            author_id = row[2]
            author_name = self.get_author_name(author_id)

            # Construire le message avec le nom de l'auteur
            message = {
                "author_name": author_name,
                "content": row[0],
                "timestamp": row[1]
            }
            messages.append(message)
        
        self.message_manager.disconnect()
        return messages

    def display_messages(self):
        self.message_list.config(state=tk.NORMAL)
        self.message_list.delete(1.0, tk.END)  # Effacer le contenu actuel

        # Afficher chaque message dans la liste
        for message in self.messages:
            # Formatage de l'heure pour l'affichage
            formatted_time = message['timestamp'].strftime("%H:%M:%S")
            self.message_list.insert(tk.END, f"{message['author_name']} ({formatted_time}): {message['content']}\n")

        self.message_list.config(state=tk.DISABLED)

    def send_message(self):
        content = self.message_entry.get()  # Contenu du message saisi par l'utilisateur
        author_id = int(self.user_id)  # Convertir l'ID d'utilisateur en entier
        self.message_manager.create_message(content, author_id, self.channel_id)
        # Actualiser les messages affichés
        self.messages = self.load_messages()
        self.display_messages()
        self.message_entry.delete(0, tk.END)  # Effacer le champ de saisie après l'envoi


if __name__ == "__main__":
    # Exemple d'utilisation de ChatApp avec ID utilisateur et ID de canal
    root = tk.Tk()
    user_id = 43  # ID de l'utilisateur connecté
    channel_id = 1  # ID du canal auquel l'utilisateur est connecté
    
    chat_app = ChatApp(root, user_id, channel_id)
    root.mainloop()