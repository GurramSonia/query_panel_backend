from werkzeug.security import  check_password_hash
from src.util.models import MongoUser,User
from flask import session,jsonify
import mysql.connector
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from settings import MONGO_HOST,MYSQL_HOST




def check_user_existence(username, password):
    # Check MySQL and MongoDB for user
    from src.controller import db,mongo
    print("entered into check_user_existstence")
    user_sql = db.session.query(User).filter_by(username=username).first()
    print(user_sql)
    user_mongo = mongo.db.users.find_one({"username": username})
    print(user_sql)
    
    if user_sql and check_password_hash(user_sql.password, password):
        return user_sql
    elif user_mongo and check_password_hash(user_mongo["password"], password):
        return MongoUser(user_mongo["_id"], user_mongo["username"],user_mongo["password"], user_mongo["password"], user_mongo["role"])
    return None

def check_user_existence_signup(username):
    # Check MySQL and MongoDB for user
    from src.controller import db,mongo
    print("entered into check_user_existstence")
    user_sql = db.session.query(User).filter_by(username=username).first()
    print(user_sql)
    user_mongo = mongo.db.users.find_one({"username": username})
    print(user_mongo)
    
    if user_sql:
        return user_sql
    elif user_mongo :
        return MongoUser(user_mongo["_id"], user_mongo["username"], user_mongo["email"],user_mongo["password"], user_mongo["role"])
    else:
        return None
    


def check_mail_existence_signup(mail):
    from src.controller import db,mongo
    # Check MySQL and MongoDB for user
    print("entered into check_user_existstence")
    mail_sql = db.session.query(User).filter_by(email=mail).first()
    print(mail_sql)
    mail_mongo = mongo.db.users.find_one({"email": mail})
    print(mail_mongo)
    
    if mail_sql:
        return mail_sql
    elif mail_mongo :
        return MongoUser(mail_mongo["_id"], mail_mongo["username"], mail_mongo["email"],mail_mongo["password"], mail_mongo["role"])
    else:
        return None

def create_user_in_mysql(username, email, password, role,original_pass):
    from src.controller import db,mongo
    print("entered into mysql ")
    new_user_sql = User(username=username, email=email, password=password, role=role,originalpass=original_pass)
    print(f"Created new user: {new_user_sql}")
    try:
        db.session.add(new_user_sql)  # Corrected from 'db.session.add("new_user", new_user_sql)'
        db.session.commit()  # Commit to MySQL
        print("User added to MySQL successfully.")
        grant_privileges(username,original_pass)
    except Exception as e:
        print(f"Error inserting into MySQL: {str(e)}")
        db.session.rollback()  # Rollback in case of error
        return ({"error": f"Error during signup: {str(e)}"}), 500
    
def create_user_in_mongo(username, email, password, role,original_pass):
    from src.controller import db,mongo
    print("entered into mongo ")
    new_user_mongo = {"username": username, "email": email, "password": password, "role": role,"original_pass":original_pass}
    print(new_user_mongo)
    mongo.db.users.insert_one(new_user_mongo)
    grant_mongodb_privileges(username, original_pass)
    print("user created into mongo")

def get_user_details_by_id(user_id):
    from src.util.models import db,User
    user = User.query.filter_by(id=user_id).first()
    if user:
        # Returning user details as a dictionary
        return {
            "username": user.username,
            "email": user.email,
            "role": user.role  # Fetching the role field from the user
        }
    return None


db_config_service= {
    "host": "mysql-service",
    "user": "GurramSonia",  # Change to your MySQL admin user
    "password": "Ramya772819390",  # Change to your MySQL root password
    "database": "querydatabase2"
}

db_config_local= {
    "host": "localhost",
    "user": "root",  # Change to your MySQL admin user
    "password": "Sonia@77281",  # Change to your MySQL root password
    "database": "querydatabase2"
}

def grant_privileges(username,original_pass):
    try:
        print("entered into priviledges")
        if MYSQL_HOST == 'localhost':
            connection = mysql.connector.connect(**db_config_local)
        else:
            connection = mysql.connector.connect(**db_config_service)
        cursor = connection.cursor()

      
        cursor.execute(f"SELECT COUNT(*) FROM mysql.user WHERE user = '{username}'")
        user_exists = cursor.fetchone()[0] > 0  # Returns True if user exists

        if user_exists:
            # If user exists, update the password
            alter_user = f"ALTER USER '{username}'@'%' IDENTIFIED BY '{original_pass}'"
            cursor.execute(alter_user)
            print(f"Password updated for user '{username}'.")
        else:
            # If user does not exist, create the user
            create_user = f"CREATE USER '{username}'@'%' IDENTIFIED BY '{original_pass}'"
            cursor.execute(create_user)
            print(f"User '{username}' created.")
        grant_query = f"GRANT ALL PRIVILEGES ON *.* TO '{username}'@'%' WITH GRANT OPTION;" 
        cursor.execute(grant_query)  # Execute grant command

        connection.commit()  # Apply changes
        cursor.execute("FLUSH PRIVILEGES;")  # Refresh privileges
        connection.commit()

        print("Permissions granted successfully for all users!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def grant_mongodb_privileges(username, password):
    try:
        print("Entering privilege granting process in MongoDB...")

        # Connect to MongoDB with authentication
        if MONGO_HOST=='loalhost':
            mongo_uri = "mongodb://ramya:Ramya772@localhost:27017/admin"
        else:
            mongo_uri = "mongodb://ramya:Ramya772@mongo-service:27017/admin"

        client = MongoClient(mongo_uri)  # Authenticated connection

        db = client.admin  # Admin database

        # Run usersInfo command after authentication
        users = db.command("usersInfo")
        print("Existing users:", users)

        # Check if the user already exists
        existing_users = db.command("usersInfo", username)
        if existing_users.get("users"):
            print(f"User '{username}' already exists.")
            db.command("updateUser", username, pwd=password)
            print(f"Password updated successfully for MongoDB user '{username}'")
            return

        # Create the user with root privileges
        db.command(
            "createUser",
            username,
            pwd=password,
            roles=[{"role": "root", "db": "admin"}]  # Assign root role
        )

        print(f"User '{username}' created successfully with root privileges.")

    except PyMongoError as err:
        print(f"Error: {err}")

    finally:
        client.close()  # Ensure connection is closed