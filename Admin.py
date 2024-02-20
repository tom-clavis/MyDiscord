import os
import bcrypt
from UserManager import UserManager

mdp = os.getenv("mdp")
class Admin():
    def __init__(self, user_manager):
        self.user_manager = user_manager
        
    def delete_user_by_email(self, email):
            self.user_manager.connect()
            sql = "DELETE FROM user WHERE email = %s"
            self.user_manager.cursor.execute(sql, (email,))
            self.user_manager.connection.commit()
            self.user_manager.disconnect()
        
    def create_user(self, first_name, last_name, email, password, id_user):
        existing_user = self.user_manager.read_user(email)
        if existing_user:
            return
        self.user_manager.connect()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql = "INSERT INTO user (first_name, last_name, email, password, id_user) VALUES (%s, %s, %s, %s, %s)"
        val = (first_name, last_name, email, hashed_password, id_user)
        self.user_manager.cursor.execute(sql, val)
        self.user_manager.connection.commit()
        self.user_manager.disconnect()
             
if __name__ == "__main__":
    host = 'localhost'
    user = 'root'
    password = mdp
    database = 'MyDiscord'
    user_manager = UserManager(host, user, password, database)

    gerer_user = Admin(user_manager)
    gerer_user.create_user("bibi", "titi", "bobo@example.com", "111", 2)
    gerer_user.delete_user_by_email("bobo@example.com")

    

   
