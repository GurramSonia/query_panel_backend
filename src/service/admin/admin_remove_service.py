from sqlalchemy import text

def remove_user_service(group_name,username):
    try:
        from src.controller import db
        print(username,group_name,"in service")
        query = text("""
    UPDATE groups_names 
    SET users = CASE 
        WHEN REPLACE(CONCAT(',', users, ','), CONCAT(',', :user_to_remove, ','), ',') = ',' THEN NULL
        ELSE TRIM(BOTH ',' FROM REPLACE(CONCAT(',', users, ','), CONCAT(',', :user_to_remove, ','), ',')) 
    END
    WHERE group_name = :group_name;
""")
        db.session.execute(query, {"user_to_remove": username, "group_name": group_name})
        db.session.commit()
        return {"message": f"User {username} removed from group {group_name}"}, 200
    except Exception as e:
        print("Error removing user:", str(e))  # Print error for debugging
        return {'error': 'Error in removing  the user'}, 500
    
def remove_group_service(group_name):
    try:
        from src.controller import db
        print(group_name,"in service")
        query = text("""    DELETE from groups_names WHERE group_name = :group_name; """)
        query1= text(""" DELETE from groups_permissions_table WHERE `group` = :group_name; """)
        db.session.execute(query, { "group_name": group_name})
        db.session.commit()
        db.session.execute(query1, { "group_name": group_name})
        db.session.commit()
        return {"message": f"  group {group_name} removed from group management"}, 200
    except Exception as e:
        print("Error removing group:", str(e))  # Print error for debugging
        return {'error': 'Error in removing  the group'}, 500
    
def remove_user_usermanagement_service(username):
    try:
        from src.controller import db
        print(username,"in service")
        query = text(""" DELETE from user_permissions_table1 WHERE username = :user_name;""")
        db.session.execute(query, {"user_name": username})
        db.session.commit()
        return {"message": f"User {username} removed from  usermanagement"}, 200
    except Exception as e:
        print("Error removing user:", str(e))  # Print error for debugging
        return {'error': 'Error in removing  the user'}, 500
    
def remove_group_operation_service(group_name,source,database,table,operation):
    try:
        from src.controller import db
        query = text("""
            UPDATE groups_permissions_table
            SET operations = CASE 
                WHEN REPLACE(CONCAT(',', operations, ','), CONCAT(',', :operation_to_remove, ','), ',') = ',' THEN NULL
                ELSE TRIM(BOTH ',' FROM REPLACE(CONCAT(',', operations, ','), CONCAT(',', :operation_to_remove, ','), ',')) 
            END
            WHERE `group` = :group_name 
            AND source = :source 
            AND databases_names = :database 
            AND table_name = :table;
        """)

        # Execute the query with parameters
        db.session.execute(query, { "operation_to_remove": operation, "group_name": group_name,"source": source,
            "database": database,"table": table})
        db.session.commit()
        return ({"message": f"Operation '{operation}' removed from table '{table}' in group '{group_name}'"}), 200
    except Exception as e:
        print("Error in removing operation:", str(e))  # Print error for debugging
        return {'error': 'Error in removing  the operation'}, 500
     
def remove_user_operation_service(user_name,source,database,table,operation):
    try:
        from src.controller import db
        query = text("""
            UPDATE user_permissions_table1 
            SET operations = CASE 
                WHEN REPLACE(CONCAT(',', operations, ','), CONCAT(',', :operation_to_remove, ','), ',') = ',' THEN NULL
                ELSE TRIM(BOTH ',' FROM REPLACE(CONCAT(',', operations, ','), CONCAT(',', :operation_to_remove, ','), ',')) 
            END
            WHERE `username` = :user_name 
            AND source = :source 
            AND databases_names = :database 
            AND table_name = :table;
        """)
         # Execute the query with parameters
        db.session.execute(query, {"operation_to_remove": operation,"user_name": user_name,
         "source": source,"database": database,"table": table })
        db.session.commit()
        return ({"message": f"Operation '{operation}' removed from table '{table}' in group '{user_name}'"}), 200
    except Exception as e:
        print("Error in removing operation:", str(e))  # Print error for debugging
        return {'error': 'Error in removing  the operation'}, 500

    

