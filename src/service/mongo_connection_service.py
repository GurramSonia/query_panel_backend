from datetime import datetime
from pymongo import MongoClient
from src.util.helpers import convert_objectid_and_datetime
from flask import session,flash,get_flashed_messages
from src.util.models import AuditLog,UserPermission,Permission
from sqlalchemy import text

def execute_mongo_query(query, connection_uri,connection_uris):
    """Execute MongoDB queries (find & DML operations)."""
   
    client = MongoClient(connection_uri)
    db = client.get_database()
    db_name = connection_uri.split("/")[-1].split("?")[0]
    collection_names = db.list_collection_names()
    print("collection_nmaes",collection_names)
    username = session.get('user_name', 'Unknown User')
    role = session.get('role')
    timestamp = datetime.utcnow()
    results = None  # Initialize results to avoid reference errors
    flash_messages = None  # Initialize flash_messages

    # Extract collection name from query
    if '.' in query and '(' in query and 'find' in query:
        parts = query.split('.')
        collection_name = parts[1].split('(')[0]
    elif ".drop()" in query:
        parts = query.split('.')
        collection_name = parts[-2] if len(parts) >= 3 else None
    elif '.' in query and '(' in query:
        parts = query.split('.')
        collection_name = parts[1]
    
    # Execute query
    if collection_name in collection_names:
        from src.controller import db as dbs,mongo
        if 'find' in query:
            result = eval(query)
            results=convert_objectid_and_datetime(list(result))
            user_permission = dbs.session.query(UserPermission).filter_by(username=username).first()
            if not user_permission:
                    from src.controller import db, mongo
                    query_string = text("""
            SELECT group_name
            FROM groups_names
            WHERE FIND_IN_SET(:username, users) > 0
        """)
        
        # Execute the query
                    result = db.session.execute(query_string, {"username": username}).fetchone()
                    group_name = result[0] if result else None
                    print("User group:", group_name)
                    user_permission = db.session.query(Permission).filter_by(group=group_name).first()
            if user_permission is None:
                print(f"No permissions found for user: {username}")
                can_view_email = False
                can_view_pass = False
            else:
                can_view_email = user_permission.view_email
                can_view_pass = user_permission.view_pass

            print("Can View Password:", can_view_pass)
            print("Can View Email:", can_view_email)
            print("Username:", username)
            for row in results:
                        if not can_view_email and 'email' in row:
                            del row['email']
                        if not can_view_pass and 'password' in row:
                            del row['password']
                        if 'original_pass' in row:
                             del row['original_pass']

        elif any(op in query for op in ["insert_one", "insert_many", "update_one", "update_many", "delete_one", "delete_many", "drop",'create_collection']):
            print("enterd into mongo execute")
            eval(query)
            results=[]
            flash(f"MongoDB {query.split('(')[0]} query executed successfully")
        else:
            print("unexpected error")
            return({"error":"Invalid mongodb queryFormat"})
            
        action=f"{query}"
        print("action is",action)
        print(db_name, "is database")
        print("DB Session Type:", type(db.session))  # Should be SQLAlchemy session
        log = AuditLog(username=username, action=action,database_name=db_name,connection_string=connection_uris)
        print(log)
        dbs.session.add(log)
        dbs.session.commit()
        mongo.db.audit_logs.insert_one({
        "username": username,
        "query": action,
        "database_name":db_name,
        "timestamp": timestamp,

    })
        flash_messages = get_flashed_messages() 
        return {"results": results, "flash_messages": flash_messages}
    else:
        return {"error": "Collection does not exist"}, 400
