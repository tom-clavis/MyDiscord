class User:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def login(self, email, password):
        connection = sqlite3.connect('myDiscord.sql')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM User WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()
        connection.close()
        return user

    def create_account(self):
        connection = sqlite3.connect('myDiscord.sql')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO User (first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
                    (self.first_name, self.last_name, self.email, self.password))
        connection.commit()
        connection.close()

    def logout(self):
        # Déconnexion de l'utilisateur
        pass

    def has_permission(self, channel_id):
        # Vérifier si l'utilisateur a les droits pour accéder au canal
        pass

