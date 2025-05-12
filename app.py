from flask import Flask
from flask_cors import CORS
from settings import FLASK_DEBUG
from src.controller import init_app

# Create Flask app
#app = Flask(__name__)
app = Flask(__name__, static_folder='static', template_folder='templates')

# Enable CORS
CORS(app,origins="*", supports_credentials=True)
""" CORS(
    app,
    origins=[
        "http://10.204.0.22:3000",
        "http://localhost:3000",
        "http://a862de0c00aea498b8162d1a7c410d0b-1175022926.us-east-1.elb.amazonaws.com",
        "http://devops.altimetrik.io",
        "https://frontend-service.query-panel.svc.cluster.local:3000/query-ui",
        "http://frontend-service.query-panel.svc.cluster.local:3000/query-ui",
        "https://frontend-service.query-panel.svc.cluster.local:80/query-ui",
        "http://frontend-service.query-panel.svc.cluster.local:80/query-ui"
        
    ],
    supports_credentials=True
    ) """
# Initialize app
init_app(app)

def create_mysql_user():
    connection = pymysql.connect(
        host="mysql-service",
        user="GurramSonia",
        password="Ramya772819390",
        database="querydatabase2"
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE USER IF NOT EXISTS 'GurramSonia'@'%' IDENTIFIED BY 'Ramya772819390';")
            cursor.execute("GRANT ALL PRIVILEGES ON *.* TO 'GurramSonia'@'%';")
            cursor.execute("FLUSH PRIVILEGES;")
        connection.commit()
    finally:
        connection.close()

def connect_and_authenticate_mongodb():
    client = MongoClient("mongodb://ramya:ramya772@mongo-service:27017/")
    
    try:
        # Check connection and authentication
        db = client.admin
        db.command("ping")
        print("✅ MongoDB authenticated successfully")
    except Exception as e:
        print("❌ Failed to authenticate:", e)
connect_and_authenticate_mongodb()
def create_mongo_user():
    try:
        admin_client = MongoClient("mongodb://ramya:ramya772@mongo-service:27017/")
        admin_db = admin_client["admin"]
        
        # Create only if doesn't exist
        existing_users = admin_db.command("usersInfo", "ramya")
        if not existing_users.get("users"):
            admin_db.command("createUser", "ramya", pwd="ramya772", roles=[{"role": "root", "db": "admin"}])
            print("✅ MongoDB user 'ramya' created.")
        else:
            print(" MongoDB user 'ramya' already exists.")
    except Exception as e:
        print("❌ Error creating MongoDB user:", e)
def init_database():
    create_mysql_user()
    create_mongo_user()
    connect_and_authenticate_mongodb()

init_database()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=FLASK_DEBUG)
