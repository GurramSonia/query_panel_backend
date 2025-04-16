from sqlalchemy import text
from werkzeug.security import  check_password_hash
from sqlalchemy.exc import SQLAlchemyError


def assign_group_permissions(group,source,databases_names,table_name,operations,view_email,view_pass):
     from src.util.models import db,Permission
     try: 
            new_permission = Permission(
                group=group,
                source=source,
                databases_names=databases_names,
                table_name=table_name,
                operations=operations,
                view_email=view_email,
                view_pass=view_pass
            )
            db.session.add(new_permission)
            db.session.commit()
            return {'message': 'group Permission created successfully'}, 201
     except SQLAlchemyError as e:
            print("error")
            db.session.rollback()
            print("SQLAlchemy Error:", str(e))  # Print the exact error
            return {"error": f"Error occurred while adding permissions: {str(e)}"}, 400
     
def assign_user_permissions(username,source,db_name,table_name,operations,view_email,view_pass):
     from src.util.models import db,UserPermission
     try:
          new_permission = UserPermission(
                username=username,
                source=source,
                databases_names=db_name,
                table_name=table_name,
                operations=operations,
                view_email=view_email,
                view_pass=view_pass
                
            )
          db.session.add(new_permission)
          db.session.commit()
          return {'message': 'user Permission created successfully'}, 201
     except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': f'Database error: {str(e)}'}, 500
     
def assign_add_group_permissions(group_name,users):
    from src.util.models import db,Group
    try:
        add_group=Group(group_name=group_name,users=users)
        db.session.add(add_group)
        db.session.commit()
        return {'message': 'Permission created successfully'}, 200
    except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'users is already there'}, 500
    
def get_available_databases_db(username):
    from src.util.models import db,Group,Permission,UserPermission,AuditLog
    try:
        query_string = text("""
            SELECT group_name
            FROM groups_names
            WHERE FIND_IN_SET(:username, users) > 0
        """)
        permission = UserPermission.query.filter_by(username=username).all()
        if  permission:
             databases = list({permission.source for permission in permission})
             return databases
        # Execute the query
        result = db.session.execute(query_string, {"username": username}).fetchone()
        group_name = result[0] if result else None
        print("User group:", group_name)
        user_permission = Permission.query.filter_by(group=group_name).all()
        databases=list({permission.source for permission in user_permission})
        connection_string=AuditLog.query.filter_by(username=username).all()

        return databases
    except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': f'Database error: {str(e)}'}, 500
def get_available_databases_names_db(username,database):
    from src.util.models import db,Group,Permission,UserPermission,AuditLog
    try:
        query_string = text("""
            SELECT group_name
            FROM groups_names
            WHERE FIND_IN_SET(:username, users) > 0
        """)
        permission = UserPermission.query.filter_by(username=username,source=database).all()
        if  permission:
             databases = list({permission.databases_names for permission in permission})
             return databases
        # Execute the query
        result = db.session.execute(query_string, {"username": username,"databases_names":database}).fetchone()
        group_name = result[0] if result else None
        print("User group:", group_name)
        user_permission = Permission.query.filter_by(group=group_name,source=database).all()
        databases=list({permission.databases_names for permission in user_permission})
        connection_string=AuditLog.query.filter_by(username=username).all()

        return databases
    except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': f'Database error: {str(e)}'}, 500
    
def get_available_connections_db(username,database):
    try:
        # Query distinct connection strings for the given username
        from src.util.models import db, AuditLog
        from sqlalchemy.exc import SQLAlchemyError
        connections = (
            db.session.query(AuditLog.connection_string)
            .filter_by(username=username)
            .all()
        )
        
        # Extract connection strings from the query result
        connection_list = [conn.connection_string for conn in connections]
        if database.lower() == "mysql":
            filtered_connections = [conn for conn in connection_list if "3306" in conn]
        elif database.lower() == "mongodb":
            filtered_connections = [conn for conn in connection_list if "27017" in conn]
        else:
            filtered_connections = connection_list  # Return all if no specific database type

        print(filtered_connections)
        return filtered_connections
        #print(connection_list)
        #return connection_list
    except SQLAlchemyError as e:
        db.session.rollback()
        return {'error': f'Database error: {str(e)}'}, 500
    




    