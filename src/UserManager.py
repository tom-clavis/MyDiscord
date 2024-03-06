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
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        sql = "INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        val = (first_name, last_name, email, hashed_password)
        self.cursor.execute(sql, val)
        self.connection.commit()
        self.disconnect()

    def read_user(self, email):
        self.connect()
        sql = "SELECT user.id, user.first_name, user.last_name, user.email, user.password, IFNULL(role.nom, 'Aucun rôle') AS role_nom FROM user LEFT JOIN role ON user.id_user = role.id WHERE email = %s;"
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
    
    def update_role_user(self, user_id, new_role_id):
        authenticated_user = self.authenticate_user("bobo@example.com", "test")
        if authenticated_user:
            user_role = authenticated_user[4]  
            if user_role == "admin" or user_role == "officier":  
                self.connect()
                sql = "UPDATE user SET id_user = %s WHERE id = %s"
                self.cursor.execute(sql, (new_role_id, user_id))
                self.connection.commit()
                self.disconnect()
            else:
                print("Vous n'avez pas les autorisations nécessaires pour effectuer cette action.")
        else:
            print("L'authentification a échoué.")
    
if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'
    user_manager = UserManager(host, user, password, database)
    

