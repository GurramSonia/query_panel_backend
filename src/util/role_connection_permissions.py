from src.util.models  import Permission,Group,UserPermission
from sqlalchemy import text
from flask import session

def check_query_permission(role, query, database,name,mysql_db_name,mongo_db_name):
    print(name) 
    if not query:
        return False
    if "create_collection" in query.lower() and database == 'mongodb':
        return True
    if "create" in query.lower() and database == 'mysql':
        return True

    user_permissions = UserPermission.query.filter_by(username=name).all()

    if  user_permissions:
         allowed_tables = [perm.table_name for perm in user_permissions]
         print("allowed tables",allowed_tables)
         allowed_operations = set()
         from src.controller import db, mongo
         for perm in user_permissions:
            operations = perm.operations.split(',')  # Convert comma-separated string back to a list
            allowed_operations.update(operations)
            allowed_databases=[perm.databases_names  for perm in  user_permissions]
            allowed_databases = [db for db in allowed_databases if db]
            print("allowed_operations",allowed_operations)
            print("allowed database are",allowed_databases)
    else:
        from src.controller import db, mongo
        query_string = text("""
            SELECT group_name
            FROM groups_names
            WHERE FIND_IN_SET(:username, users) > 0
        """)
        
        # Execute the query
        result = db.session.execute(query_string, {"username": name}).fetchone()
        group_name = result[0] if result else None
        print("User group:", group_name)
        user_permission = Permission.query.filter_by(group=group_name).all()
        allowed_operations= set()
        from src.controller import db, mongo
        for perm in user_permission:
            operations = perm.operations.split(',')  # Convert comma-separated string back to a list
            allowed_operations.update(operations)
            print("allowed_operation is",allowed_operations)
            allowed_tables = [perm.table_name for perm in  user_permission]
            allowed_databases=[perm.databases_names  for perm in  user_permission]
            allowed_databases = [db for db in allowed_databases if db]
            print(allowed_tables,allowed_operations)
            print("allowed database are",allowed_databases)
    result = get_table_operation(database,query,mysql_db_name,mongo_db_name)
    table_name = result["table_name"]
    operation = result["operation"]
    database_name = result["database_name"]
 

    
    print(database_name in allowed_databases)
    return operation in allowed_operations and table_name in allowed_tables and database_name in allowed_databases

def get_table_operation(database,query,mysql_db_name,mongo_db_name):
    if database=="mysql":
        query_upper = query.upper()
        query_parts = query.split()
        database_name=mysql_db_name
        print("database_name is",database_name)
        if 'DROP' in query_upper:
            operation = 'DROP'
            table_name = query_parts[query_upper.split().index("DROP") + 2]
            print("Operation:", operation, "Table:", table_name)
        elif 'SELECT' in query_upper and 'FROM ' in query_upper:
            operation = 'SELECT'
            table_name = query_parts[query_upper.split().index("FROM") + 1]
            print("Operation:", operation, "Table:", table_name)
        elif 'DELETE' in query_upper:
            operation = 'DELETE'
            table_name = query_parts[query_upper.split().index("FROM") + 1]
            print("Operation:", operation, "Table:", table_name)
        elif 'INSERT' in query_upper:
            operation = 'INSERT'
            table_name = query_parts[query_upper.split().index("INTO") + 1].split('(')[0]
            print("Operation:", operation, "Table:", table_name)
        elif 'UPDATE' in query_upper:
            operation = 'UPDATE'
            table_name = query_parts[query_upper.split().index("UPDATE") + 1]
            print("Operation:", operation, "Table:", table_name,"database_name:",database_name)
        return {"table_name":table_name,"operation":operation,"database_name":database_name}
    
    elif database == 'mongodb':
        # Parse MongoDB queries
        operation = None
        table_name = None
        database_name=mongo_db_name

        # Example query: mongo.db.users.find({})
        if ".drop()" in query:
            operation = "drop"
            parts = query.split('.')
            table_name = parts[-2] if len(parts) >= 3 else None
        
        elif '.' in query and '(' in query:
              parts = query.split('.') # Split into parts: ['mongo', 'db', 'users', 'insert_one({...})']# Split into parts: ['mongo', 'db', 'users', 'insert_one({...})']
              print("Parts:", parts)
              table_name = parts[1]  # Collection name is the 3rd part (index 2)
              operation_with_args = parts[2]
              print("args",operation_with_args)  # The last part has operation and arguments

                # Extract the operation before '('
              operation = operation_with_args.split('(')[0]
        elif '.' in query and '(' in query and 'find' in query :
            # Extract `db.collection.method`
            parts = query.split('.')
            print(parts)
            print(len(parts))
            if len(parts) >= 2:
                table_name = parts[1].split('(')[0]  # Get collection name
                operation = parts[-1].split('(')[0]  
                print(table_name,operation)
                print("parts are",parts)

        print("Extracted table_name:", table_name)
        print("Extracted operation:", operation)
        print("Extracted database_name:", database_name)
        return {"table_name":table_name,"operation":operation,"database_name":database_name}
        
    else:
        return False
        