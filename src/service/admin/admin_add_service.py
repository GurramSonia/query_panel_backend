from src.util.models import  Permission,Group,UserPermission
from src.util.admin_utils import assign_group_permissions,assign_user_permissions
from sqlalchemy import text

def process_permission_service(data):
    try:
        print(data)
        source = data.get('source')
        table_name = data.get('tableName')
        operations = ','.join(data.get('operations'))
        group=data.get('group') 
        databases_names=data.get('db_name')
        view_email=data.get('view_email') 
        view_pass=data.get('view_pass')# Convert operations list to comma-separated string
        view_email = bool(view_email) if view_email is not None else False
        view_pass = bool(view_pass) if view_pass is not None else False
 
        if not all([source, table_name, operations,group,databases_names]):
            return {'error': 'All fields are required'}, 400
        
        # Check for existing permissions
        existing_permission = Permission.query.filter_by(group=group, source=source,databases_names=databases_names, table_name=table_name ).first()
        if existing_permission:
            return {'error': 'Permissions already exist for this user, source, and table'}, 400
        
        # Assign permissions
        result = assign_group_permissions(group, source,databases_names, table_name, operations,view_email,view_pass)
        print("result is",result)
        return result
    except Exception as e:
        print(f"Error in adding permission: {e}")
        return {"error": "An error occurred"}, 500

def process_user_permission_service(data):
    try:
        print(data)
        username=data.get('username')
        source = data.get('source')
        databases_names=data.get('db_name')
        table_name = data.get('tableName')
        operations = ','.join(data.get('operations'))
        view_email=data.get('view_email')
        view_pass=data.get('view_pass')

        if not all([username,source, table_name, operations]):
            return {'error': 'All fields are required'}, 400
        
        # Check for existing permissions
        existing_permission = UserPermission.query.filter_by(username=username, source=source,databases_names=databases_names, table_name=table_name ).first()
        if existing_permission:
            return {'error':  f'Permissions already exist for this user: username={username}, source={source},database={databases_names} table={table_name}'}, 400
        
        # Assign permissions
        result = assign_user_permissions(username, source, databases_names, table_name, operations,view_email,view_pass)
        print("result is",result)
        if result:
            return {"message": "Permission added successfully"}, 201
        else:
            return {"error": "Failed to add permission"}, 400
    except Exception as e:
        print(f"Error in adding permission: {e}")
        return {"error": "An error occurred"}, 500
    
def group_creation_service(data):
    try:
        from src.util.admin_utils import assign_add_group_permissions
        group_name= data.get('groupName')
        users = ','.join(data.get('users'))
        if not all([group_name,users]):
            return {'error': 'All fields are required'}, 400
        existing_permission = Group.query.filter_by(group_name=group_name).first()
        if existing_permission:
            return {'error': 'group name is already present'}, 400
        result = assign_add_group_permissions(group_name,users)
        return result
    except Exception as e:
        print(f"Error in adding permission: {e}")
        return {"error": "An error occurred"}, 500


def add_user_service(group_name, username):
    try:
        from src.controller import db
        print(username, group_name, "in service")
        query = text("""
        UPDATE groups_names
        SET users = CASE
            WHEN users IS NULL THEN :user_to_add
            ELSE CONCAT(users, ',', :user_to_add)
        END
        WHERE group_name = :group_name;
        """)
        db.session.execute(query, {"user_to_add": username, "group_name": group_name})
        db.session.commit()
        return {"message": f"User {username} added to group {group_name}"}, 200
    except Exception as e:
        print("Error adding user:", str(e))  # Print error for debugging
        return {'error': 'Error in adding the user'}, 500
    
def add_group_operation_service(group_name,source,database,table,operation):
    try:
        from src.controller import db
        query = text("""
            UPDATE groups_permissions_table
SET operations = 
    CASE 
        WHEN operations IS NULL OR operations = '' THEN :operation_to_add
        WHEN FIND_IN_SET(:operation_to_add, operations) = 0 THEN CONCAT(operations, ',', :operation_to_add)
        ELSE operations 
    END
WHERE `group` = :group_name 
AND source = :source 
AND databases_names = :database 
AND table_name = :table;
        """)
        db.session.execute(query, {"operation_to_add": operation,"group_name": group_name,"source": source,"database": database,"table": table })
        db.session.commit()
        return ({"message": f"Operation '{operation}' added table '{table}' in group '{group_name}'"}), 200
    except Exception as e:
        print("Error in adding operation:", str(e))  # Print error for debugging
        return {'error': 'Error in adding the operation'}, 500
     
def add_user_operation_service(user_name,source,database,table,operation):
    try:
        from src.controller import db
        query = text("""
            UPDATE user_permissions_table1
SET operations = 
    CASE 
        WHEN operations IS NULL OR operations = '' THEN :operation_to_add
        WHEN FIND_IN_SET(:operation_to_add, operations) = 0 THEN CONCAT(operations, ',', :operation_to_add)
        ELSE operations 
    END
WHERE `username` = :user_name 
AND source = :source 
AND databases_names = :database 
AND table_name = :table;
        """)
        db.session.execute(query, {"operation_to_add": operation,"user_name": user_name,"source": source,"database": database,"table": table })
        db.session.commit()
        return ({"message": f"Operation '{operation}' added table '{table}' in group '{user_name}'"}), 200
    except Exception as e:
        print("Error in adding operation:", str(e))  # Print error for debugging
        return {'error': 'Error in adding the operation'}, 500


