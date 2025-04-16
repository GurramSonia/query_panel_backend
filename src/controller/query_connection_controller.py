import mysql.connector
from flask import  request, session
from flask_restx import Namespace, Resource, fields
from urllib.parse import urlparse
from urllib.parse import urlparse
from src.util.role_connection_permissions import check_query_permission
from src.service.mysql_connection_service import execute_mysql_query
from src.service.mongo_connection_service import execute_mongo_query
from sqlalchemy import text
from pymongo import MongoClient
from settings import MONGO_HOST,MYSQL_HOST,MONGO_PORT,MYSQL_PORT
from src.util.models import MongoUser,User


connection_ns = Namespace('Dashboardconnection', description='Dashboard related operations')

query_model_connection = connection_ns.model('QueryModelConnection', {
    'query': fields.String(required=True, description='SQL or MongoDB query to be executed'),
    'database': fields.String(required=True, description='The target database type (MySQL or MongoDB)'),
    'maskedConnection': fields.String(required=True, description='The target database type (MySQL or MongoDB)')
}) 
query_model_connection_user = connection_ns.model('QueryModelConnection', {
    'query': fields.String(required=True, description='SQL or MongoDB query to be executed'),
    'database': fields.String(required=True, description='The target database type (MySQL or MongoDB)'),
    'databases_names': fields.String(required=True, description='The target database type (MySQL or MongoDB)')
}) 
query_result_model_connection = connection_ns.model('QueryResultModelConnection', {
    'results': fields.List(fields.Raw(), description='Results from the executed query'),
    'error': fields.String(description='Error message if any'),
    'flash_messages': fields.List(fields.String, description='List of flash messages for the user')
}) 
get_table_model_connection=connection_ns.model('GetTables', {
    'database': fields.String(required=True, description='The target database type (MySQL or MongoDB)'),
    'maskedConnection': fields.String(required=True, description='The target database type (MySQL or MongoDB)')
})
get_table_model_connection_user=connection_ns.model('GetTables', {
    'database': fields.String(required=True, description='The target database type (MySQL or MongoDB)'),
    'databases_names': fields.String(required=True, description='The target database type (MySQL or MongoDB)')
})

@connection_ns.route('query-connection')
class Dashboardconnection(Resource):
    @connection_ns.expect(query_model_connection)
    @connection_ns.expect(query_result_model_connection)
    def post(self):
        print("entered into connection dashboard")
        data = request.json
        print("data is",data)
        query = data.get("query")
        db_type = data.get("database")
        username = session.get('user_name')
        role = session.get('role')
        connection_uris = data.get('maskedConnection')
        print(db_type,query,connection_uris)
        if db_type == "mysql":
            print("entered into mysql")
            connection_uri = f"mysql+pymysql://{connection_uris}"
        elif db_type == "mongodb":
            connection_uri = f"mongodb://{connection_uris}"
        #connection_uri=f"mysql+pymysql://{connection_uri}"
        #connection_uri=f"mongodb://{connection_uri}"
        print(db_type,query,connection_uri)
        parsed_uri = urlparse(connection_uri)
        mysql_db_name = parsed_uri.path.lstrip('/')
        mongo_db_name = connection_uri.split("/")[-1].split("?")[0]

        if not db_type or not connection_uri:
            return ({"error": "Missing database type or connection details"}), 400
        print("check",check_query_permission(role, query, db_type, username,mysql_db_name,mongo_db_name))
        if not check_query_permission(role, query, db_type, username,mysql_db_name,mongo_db_name):
            return {'error': "You do not have permission to execute this query."}, 403
        
        try:
            if db_type == "mysql":
                return execute_mysql_query(query, connection_uri,connection_uris,db_type,mysql_db_name,mongo_db_name)
            elif db_type == "mongodb":
                return execute_mongo_query(query, connection_uri,connection_uris)
            else:
                return {"error": "Unsupported database type"}, 400
        except Exception as e:
            print("error")
            print("error occuring during executing command")
            return {"error": str(e)}, 500


@connection_ns.route('query-connection-user')
class Dashboardconnection(Resource):
    @connection_ns.expect(query_model_connection_user)
    @connection_ns.expect(query_result_model_connection)
    def post(self):
        from src.controller import db,mongo
        print("entered into check_user_existstence")
    
        print("entered into connection dashboard")
        data = request.json
        print("data is",data)
        query = data.get("query")
        db_type = data.get("database")
        databases_names=data.get("databases_names")
        username = session.get('user_name')
        user_sql = db.session.query(User).filter_by(username=username).first()
        print(user_sql)
        password = user_sql.originalpass if user_sql else None
        role = session.get('role')
        print(db_type,query,databases_names)
        if db_type == "mysql":
            print("entered into mysql")
            connection_uri = f"mysql+pymysql://{username}:{password}@{MYSQL_HOST}:{MYSQL_PORT}/{databases_names}"
            connection_uris=f"{username}:{password}@{MYSQL_HOST}:{MYSQL_PORT}/{databases_names}"
        elif db_type == "mongodb":
            connection_uri = f"mongodb://{username}:{password}@{MONGO_HOST}:{MONGO_PORT}/{databases_names}?authSource=admin"
            connection_uris=f"{username}:{password}@{MONGO_HOST}:{MONGO_PORT}/{databases_names}?authSource=admin"
        #connection_uri=f"mysql+pymysql://{connection_uri}"
        #connection_uri=f"mongodb://{connection_uri}"
        print(db_type,query,connection_uri)
        parsed_uri = urlparse(connection_uri)
        mysql_db_name = parsed_uri.path.lstrip('/')
        mongo_db_name = connection_uri.split("/")[-1].split("?")[0]

        if not db_type or not connection_uri:
            return ({"error": "Missing database type or connection details"}), 400
        print("check",check_query_permission(role, query, db_type, username,mysql_db_name,mongo_db_name))
        if not check_query_permission(role, query, db_type, username,mysql_db_name,mongo_db_name):
            return {'error': "You do not have permission to execute this query."}, 403
        
        try:
            if db_type == "mysql":
                return execute_mysql_query(query, connection_uri,connection_uris,db_type,mysql_db_name,mongo_db_name)
            elif db_type == "mongodb":
                return execute_mongo_query(query, connection_uri,connection_uris)
            else:
                return {"error": "Unsupported database type"}, 400
        except Exception as e:
            print("error")
            print("error occuring during executing command")
            return {"error": str(e)}, 500
        
@connection_ns.route('get-tables')
class GetTables(Resource):
    @connection_ns.expect(get_table_model_connection)
   
    def post(self):
        print("entered into connection tables")
        data = request.json
        print("data is",data)
        db_type = data.get("database")
        connection_uris = data.get("maskedConnection")

       
        conn = None 
        #from src.service.mysql_connection_service import get_mysql_connection
        try:
            if db_type == "mysql":
                connection_uri = f"mysql+pymysql://{connection_uris}"
                conn,database=get_mysql_connection(connection_uri)
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                print("tables are",tables)
                conn.close()
                return ({"tables":tables})
            elif db_type=="mongodb":
                 connection_uri = f"mongodb://{connection_uris}"
                 client = MongoClient(connection_uri)
                 db = client.get_database()
                 db_name = connection_uri.split("/")[-1].split("?")[0]
                 collection_names = db.list_collection_names()
                 return ({"tables":collection_names})
                 
    
            else:
                return {"error": "Unsupported database type"}, 400
        except Exception as e:
            print("error",str(e))
            return {"error": str(e)}, 500

        finally:
            if conn:
                conn.close() 

@connection_ns.route('get-tables-user')
class GetTables(Resource):
    @connection_ns.expect(get_table_model_connection_user)
   
    def post(self):
        from src.controller import db,mongo
        print("entered into connection tables")
        data = request.json
        print("data is",data)
        db_type = data.get("database")
        database=data.get("databases_names")
        username = session.get('user_name')
        user_sql = db.session.query(User).filter_by(username=username).first()
        print(user_sql)
        password = user_sql.originalpass if user_sql else None

       
        conn = None 
        #from src.service.mysql_connection_service import get_mysql_connection
        try:
            if db_type == "mysql":
                connection_uris=f"{username}:{password}@{MYSQL_HOST}:{MYSQL_PORT}/{database}"
                connection_uri = f"mysql+pymysql://{connection_uris}"
                conn,database=get_mysql_connection(connection_uri)
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                print("tables are",tables)
                conn.close()
                return ({"tables":tables})
            elif db_type=="mongodb":
                 #mongodb://ramya:Ramya772@localhost:27017/mongo-database?authSource=admin
                 connection_uris=f"{username}:{password}@{MONGO_HOST}:{MONGO_PORT}/{database}?authSource=admin"
                 connection_uri = f"mongodb://{username}:{password}@{MONGO_HOST}:{MONGO_PORT}/{database}?authSource=admin"
                 client = MongoClient(connection_uri)
                 print("connection_uris",connection_uri,connection_uris)
                 db = client.get_database()
                 db_name = connection_uri.split("/")[-1].split("?")[0]
                 
                 collection_names = db.list_collection_names()
                 return ({"tables":collection_names})
                 
    
            else:
                return {"error": "Unsupported database type"}, 400
        except Exception as e:
            print("error in mongo collections",str(e))
            return {"error": str(e)}, 500

        finally:
            if conn:
                conn.close() 


@connection_ns.route('previous-queries')
class GetTables(Resource):
    def post(self):
        print("entered into connection dashboard")
        data = request.json
        db_type = data.get("database")
        try:
             from src.controller import db
             if db_type == "mongodb":
                query= text(""" SELECT action from audit_log  where action LIKE 'db%' """)
             else:
                 query= text(""" SELECT action from audit_log  where action NOT LIKE 'db%' """)
             result = db.session.execute(query).fetchall()
             query_list = [query[0] for query in result]
             print(query_list)
             previous_queries=query_list
            
             return ({"queries": previous_queries})
        except Exception as e:
            print("error")
            return {"error": str(e)}, 500
def get_mysql_connection(uri):
    """Connect to MySQL using a URI."""
    parsed_uri = urlparse(uri)
    print("parse uri",parsed_uri)
    database_name = parsed_uri.path.lstrip('/')
    conn = mysql.connector.connect(
        host=parsed_uri.hostname,
        user=parsed_uri.username,
        password=parsed_uri.password,
        database=parsed_uri.path.lstrip('/'),
        port=parsed_uri.port or 3306
    )
    return conn,database_name


