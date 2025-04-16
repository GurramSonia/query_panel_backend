from sqlalchemy import text

def get_available_databases_service(username):
    """
    Fetch available databases for a given user based on their permissions.
    """
    try:
        from src.util.admin_utils import get_available_databases_db
        if not username:
            return {'error': 'Unauthorized: Username not found in session'}, 401
        databases=get_available_databases_db(username)
        return databases,200
    except Exception as e:
        print(f"Error fetching available databases: {e}")
        return {'error': 'An error occurred while fetching databases'}, 500
def get_available_connections_service(username,database):
    """
    Fetch available databases for a given user based on their permissions.
    """
    try:
        from src.util.admin_utils import get_available_connections_db
        if not username:
            return {'error': 'Unauthorized: Username not found in session'}, 401
        databases=get_available_connections_db(username,database)
        return databases,200
    except Exception as e:
        print(f"Error fetching available databases: {e}")
        return {'error': 'An error occurred while fetching databases'}, 500
def get_available_databases_names_service(username,database):
    """
    Fetch available databases for a given user based on their permissions.
    """
    try:
        from src.util.admin_utils import get_available_databases_names_db
        if not username:
            return {'error': 'Unauthorized: Username not found in session'}, 401
        databases=get_available_databases_names_db(username,database)
        return databases,200
    except Exception as e:
        print(f"Error fetching available databases: {e}")
        return {'error': 'An error occurred while fetching databases'}, 500
    

def fetch_audit_logs_service():
    """
    Fetch and format all audit logs from the database.
    """
    try:
        from src.util.models import db
        from sqlalchemy.sql import text
        from datetime import datetime
        query_str = "SELECT id, username, action, database_name, timestamp FROM audit_log"
        result = db.session.execute(text(query_str))
        columns = result.keys()
        results = [dict(zip(columns, row)) for row in result.fetchall()]
        # Format datetime values in the result
        for row in results:
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        return results, 200
    except Exception as e:
        print(f"Error fetching audit logs: {e}")
        return {'error': 'Failed to fetch audit logs'}, 500

def fetch_users_service(db):
    """
    Fetch all users with their usernames and roles.
    """
    try:
        query_str = "SELECT username, role FROM user"
        result = db.session.execute(text(query_str))
        columns = result.keys()
        # Convert rows to dictionaries
        results = [dict(zip(columns, row)) for row in result.fetchall()]
        return results, 200
    except Exception as e:
        return {'error': str(e)}, 500

def fetch_groups_service(db):
    """
    Fetch all users with their usernames and roles.
    """
    try:
        query_str= "SELECT id, group_name, users FROM  groups_names"
        result = db.session.execute(text(query_str))
        columns = result.keys()
        # Convert rows to dictionaries
        results = [dict(zip(columns, row)) for row in result.fetchall()]
        print("groups and users",results)
        return results, 200
    except Exception as e:
        return {'error': str(e)}, 500
    
def get_group_operations():
    try: 
        from src.controller import db
        query = text("""
            SELECT `group`, source,`databases_names`, table_name, operations,view_email,view_pass
            FROM groups_permissions_table
        """)
        result = db.session.execute(query).fetchall()
        # Convert flat data to hierarchical structure
        group_operations = {}
        for row in result:
            group_name, source,database, table, operations,view_email,view_pass = row
            if group_name not in group_operations:
                group_operations[group_name] = {}  # Initialize group
            if source not in group_operations[group_name]:
                group_operations[group_name][source] = {} 
            if database not in group_operations[group_name][source]:
                group_operations[group_name][source][database] = {}  # Initialize source
            #group_operations[group_name][source][database][table] = operations.split(',')  # Convert operations CSV to list
            group_operations[group_name][source][database][table] ={
                'operations': operations.split(','),  # Split CSV of operations into a list
                'view_email': view_email,
                'view_pass': view_pass
            }
        print("group_operations:", group_operations)  # Debugging
        return (group_operations), 200  # Return structured JSON
    except Exception as e:
        return ({"error": str(e)}), 500
    
def get_user_operations():
    try: 
        from src.controller import db
        query = text("""
            SELECT `username`, `source`,`databases_names`, `table_name`, `operations`,view_email,view_pass
            FROM `user_permissions_table1`
        """)
        result = db.session.execute(query).fetchall()
        # Convert flat data to hierarchical structure
        user_operations = {}
        for row in result:
            username, source, database, table, operations,view_email,view_pass = row
            if username not in user_operations:
                user_operations[username] = {}  # Initialize user
            if source not in user_operations[username]:
                user_operations[username][source] = {}  # Initialize source

            if database not in user_operations[username][source]:
                user_operations[username][source][database] = {}  # Initialize database
            #user_operations[username][source][database][table] = operations.split(',') 
            user_operations[username][source][database][table] ={
                'operations': operations.split(','),  # Split CSV of operations into a list
                'view_email': view_email,
                'view_pass': view_pass
            } # Convert operations to list
        print("user_operations:", user_operations)  # Debugging
        return (user_operations), 200  # Return structured JSON
    except Exception as e:
        return ({"error": str(e)}), 500