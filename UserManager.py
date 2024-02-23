import mysql.connector
import os
import bcrypt
from ConnectionBD import ConnectionBD

mdp = os.getenv("mdp")

class UserManager(ConnectionBD):

    def create_user(self, first_name, last_name, email, password):
        existing_user = self.read_user(email)
        if existing_user:
            return
        self.connect()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        val = (first_name, last_name, email, hashed_password)
        self.cursor.execute(sql, val)
        self.connection.commit()
        self.disconnect()

    def read_user(self, email):
        self.connect()
        sql = "SELECT user.first_name, user.last_name, user.email, IFNULL(role.nom, 'Aucun rôle') AS role_nom FROM user LEFT JOIN role ON user.id_user = role.id WHERE email = %s;"
        self.cursor.execute(sql, (email,))
        user = self.cursor.fetchone()
        self.disconnect()
        if user:
            return user
        else:
            return None
        
    def delete_user_by_email(self, email):
            self.connect()
            sql = "DELETE FROM user WHERE email = %s"
            self.cursor.execute(sql, (email,))
            self.connection.commit()
            self.disconnect()
        
    def authenticate_user(self, email, password):
        user = self.read_user(email)
        if user:
            hashed_password = user[4]  
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return user
        return None
    
        
if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'

    user_manager = UserManager(host, user, password, database)
    user_manager.create_user("bibi", "titi", "bobo@example.com", "111")
    user = user_manager.read_user("bobo@example.com")
    print(user)

