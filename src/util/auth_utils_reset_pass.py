from src.util.models import MongoUser,User
from datetime import datetime
import secrets
from datetime import datetime, timedelta
import mysql.connector
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from settings import MYSQL_USER,MYSQL_DATABASE,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_PORT,MONGO_USERNAME,MONGO_PASSWORD,MONGO_DATABASE,MONGO_HOST,MONGO_PORT


db_config_service = {
    "host": "mysql-service",
    "user": "GurramSonia",
    "password": "Ramya772819390",
    "database": "querydatabase2"
}
db_config_local= {
    "host": "localhost",
    "user": "root",  # Change to your MySQL admin user
    "password": "Sonia@77281",  # Change to your MySQL root password
    "database": "querydatabase2"
}
def check_user_existence_by_email(email):
    from src.controller import db,mongo
    user_sql = db.session.query(User).filter_by(email=email).first()
    print(user_sql)
    user_mongo = mongo.db.users.find_one({"email": email})
    print(user_mongo)
    if  user_sql:
        return user_sql
    elif user_mongo :
        return MongoUser(user_mongo["_id"], user_mongo["username"], user_mongo["email"],user_mongo["password"], user_mongo["role"])
    else:
        return None

def generate_reset_token(email):
    from src.util.models import PasswordResetToken, User,MongoUser
    from src.controller import db,mongo
     # Generate a unique reset token
    token = secrets.token_urlsafe(64)

    # Find the user (could be MySQL or MongoDB)
    user = check_user_existence_by_email(email)
    if not user:
        return None  # Shouldn't happen, since we already check in the route

    # Save the reset token to the database with the user ID
    reset_token = PasswordResetToken(
        token=token,
        user_id=user.id,
        created_at=datetime.utcnow()
    )
    db.session.add(reset_token)
    db.session.commit()
    return token 

def get_user_by_token(token):
    from src.util.models import PasswordResetToken, User
    """
    Get user by the reset token.
    If the token is valid and not expired, return the user object.
    """
    # Look for the reset token in the PasswordResetToken table
    reset_token_entry = PasswordResetToken.query.filter_by(token=token).first()
    
    if not reset_token_entry:
        return None  # Token not found
    
    # Check if the token is expired (e.g., expire after 1 hour)
    token_age = datetime.utcnow() - reset_token_entry.created_at
    if token_age > timedelta(hours=1):  # 1 hour expiration for example
        return None  # Token is expired
    
    # Return the associated user
    user = User.query.get(reset_token_entry.user_id)
    if user:
        return user
    
    return None  # User not found

def reset_user_password(user_id, hashed_password,mongo_username,password):
    from src.util.models import PasswordResetToken, User
    """
    Reset the user's password in the database.
    """
    from src.controller import db,mongo
    # Find the user by ID
    user_sql = User.query.get(user_id)
    user_mongo = mongo.db.users.find_one({"username": mongo_username})
    if user_sql is None and user_mongo is None:
        return {"error": "User not found in both MySQL and MongoDB"}, 404
    
    # Step 3: Update password in MySQL if the user exists in MySQL
    if user_sql:
        print("sqlpassword",password)
        print("entered in user_sql",user_sql.username)
        user_sql.password = hashed_password
        user_sql.originalpass=password
        db.session.commit()  # Commit the transaction to MySQL
        try:
            if MYSQL_HOST=='localhost':
                connection = mysql.connector.connect(**db_config_local)
            else:
                connection = mysql.connector.connect(**db_config_service)
            cursor = connection.cursor()

            # Alter the MySQL user password
            alter_query = f"ALTER USER '{user_sql.username}'@'%' IDENTIFIED BY '{password}';"
            cursor.execute(alter_query)
            connection.commit()
            cursor.execute("FLUSH PRIVILEGES;")  # Refresh privileges

            print(f"Password updated successfully for MySQL user '{user_sql.username}'.")

        except mysql.connector.Error as err:
         return {"error": f"MySQL error: {err}"}, 500

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    



    # Step 4: Update password in MongoDB if the user exists in MongoDB
    if user_mongo:
        print("password",password)
        print("usermongo",user_mongo["username"],password)
        mongo.db.users.update_one({"_id": user_mongo["_id"]}, {"$set": {"password": hashed_password,"original_pass":password}})
        try:
            # Connect to MongoDB Admin database (must authenticate as an admin)
            if MONGO_HOST=='localhost':
                client = MongoClient("mongodb://ramya:Ramya772@localhost:27017/admin")
            else:
                client = MongoClient("mongodb://ramya:Ramya772@mongo-service:27017/admin")
            db = client.admin  # Switch to the admin database

            # Ensure username is a string
            mongo_username = user_mongo["username"]
            if not isinstance(mongo_username, str):
                raise ValueError("MongoDB username must be a string")

            # Check if user exists
            existing_users = db.command("usersInfo", mongo_username)
            if not existing_users.get("users"):
                print(f"User '{mongo_username}' not found in MongoDB.")
            else:
                # ✅ Pass `mongo_username` (string), not `user_mongo` (object)
                db.command("updateUser", mongo_username, pwd=password)
                print(f"Password updated successfully for MongoDB user '{mongo_username}'")

        except Exception as e:
            print(f"Error updating password: {e}")
            return {"error": f"MongoDB error: {str(e)}"}, 500

        finally:
            client.close()  # Ensure connection is closed

    return {"message": "Password updated successfully in both MySQL and MongoDB"}, 200
