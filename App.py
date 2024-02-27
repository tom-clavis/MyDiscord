import tkinter as tk
import mysql.connector

class DiscordApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Discord")

        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        self.message_frame = tk.Frame(self.master)
        self.message_frame.pack()
        self.message_listbox = tk.Listbox(self.message_frame, width=50)
        self.message_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.message_frame, orient=tk.VERTICAL, command=self.message_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_listbox.config(yscrollcommand=self.scrollbar.set)

        # Connexion à la base de données MySQL
        self.connection = mysql.connector.connect(
            host="root",
            user="your_username",
            password="1234",
            database="MyDiscord.sql"
        )
        self.cursor = self.connection.cursor()

        
        
def main():
    root = tk.Tk()
    app = DiscordApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
