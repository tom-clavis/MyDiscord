import tkinter as tk
from tkinter import scrolledtext

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Discord-like Chat")
        self.master.geometry("600x400")

        # Liste statique de messages
        self.messages = [
            {"user": "User1", "content": "Hello!"},
            {"user": "User2", "content": "Hi there!"},
            {"user": "User1", "content": "How are you?"},
            # Ajoutez d'autres messages selon vos besoins
        ]

        # Zone de texte déroulante pour afficher les messages
        self.message_list = scrolledtext.ScrolledText(master, wrap=tk.WORD, state=tk.DISABLED)
        self.message_list.pack(expand=True, fill="both")

        # Entrée pour taper un nouveau message
        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(pady=10)
        
        # Bouton pour envoyer un message
        send_button = tk.Button(master, text="Send", command=self.send_message)
        send_button.pack()

        # Afficher les messages initiaux
        self.display_messages()

    def display_messages(self):
        self.message_list.config(state=tk.NORMAL)
        self.message_list.delete(1.0, tk.END)  # Effacer le contenu actuel

        # Afficher chaque message dans la liste
        for message in self.messages:
            self.message_list.insert(tk.END, f"{message['user']}: {message['content']}\n")

        self.message_list.config(state=tk.DISABLED)

    def send_message(self):
        new_message = {"user": "User1", "content": self.message_entry.get()}
        self.messages.append(new_message)
        self.display_messages()
        self.message_entry.delete(0, tk.END)  # Effacer le champ de saisie après l'envoi

if __name__ == "__main__":
    root = tk.Tk()
    chat_app = ChatApp(root)
    root.mainloop()
