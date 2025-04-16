from flask_restx import  Resource
from flask import  request
from sqlalchemy import text
from src.controller.admin.admin_ns import admin_ns_add
from src.controller.admin.admin_models import(group_model,add_group_operation,add_user_operation,add_user,group_permission_model,user_permission_model,update_email_pass)

@admin_ns_add.route('/create-group')
class GroupCreation(Resource):
    @admin_ns_add.expect(group_model)
    @admin_ns_add.response(201, 'Group created successfully')
    @admin_ns_add.response(400, 'Invalid input data')
    @admin_ns_add.response(500, 'Internal server error')
    def post(self):
        try:
            data = request.json
            from src.service.admin.admin_add_service import group_creation_service
            response, status_code =group_creation_service(data)
            return response, status_code
        except Exception as e:
            print(f"Error in fetching operations: {e}")
            return {'error': 'An unexpected error occurred while fetching operations.'}, 500 
        
@admin_ns_add.route('/group_operation_add')
class RemoveUser(Resource):
    @admin_ns_add.expect(add_group_operation)
    @admin_ns_add.response(201, 'group operation is added succesfully')
    @admin_ns_add.response(400, 'Invalid input data')
    @admin_ns_add.response(500, 'Internal server error')
    def post(self):
        try:
            from src.service.admin.admin_add_service  import add_group_operation_service
            data = request.json
            group_name = data.get("group_name")
            source = data.get("source")
            database = data.get("database")
            table = data.get("table")
            operation = data.get("operation")
            if not all([group_name, source, database, table, operation]):
             return ({"error": "Missing required parameters"}), 400
            response, status_code = add_group_operation_service(group_name,source,database,table,operation)
            return response, status_code
        except Exception as e:
            print(f"Error in adding operation into group: {e}")
            return {'error': 'An unexpected error occurred adding operation into group.'}, 500 

@admin_ns_add.route('/user_operation_add')
class RemoveUser(Resource):
    @admin_ns_add.expect(add_user_operation)
    @admin_ns_add.response(201, 'user operation is added succesfully')
    @admin_ns_add.response(400, 'Invalid input data')
    @admin_ns_add.response(500, 'Internal server error')
    def post(self):
        try:
            from src.service.admin.admin_add_service  import add_user_operation_service
            data = request.json
            user_name = data.get("user_name")
            source = data.get("source")
            database = data.get("database")
            table = data.get("table")
            operation = data.get("operation")
            if not all([user_name, source, database, table, operation]):
             return ({"error": "Missing required parameters"}), 400
            response, status_code = add_user_operation_service(user_name,source,database,table,operation)
            return response, status_code
        except Exception as e:
            print(f"Error in adding operation into group: {e}")
            return {'error': 'An unexpected error occurred adding operation into group.'}, 500 

@admin_ns_add.route('/add_user')
class AddUser(Resource):
    @admin_ns_add.expect(add_user)
    @admin_ns_add.response(201, 'user is added succesfully')
    @admin_ns_add.response(400, 'Invalid input data')
    @admin_ns_add.response(500, 'Internal server error')
    def post(self):
        try:
            from src.service.admin.admin_add_service  import add_user_service
            data = request.json
            group_name = data.get("group_name")
            username = data.get("username")
            print(group_name,username)
            if not group_name or not username:
                 return ({"error": "Missing group_name or username"}), 400
            response, status_code = add_user_service(group_name,username)
            return response, status_code
        except Exception as e:
            print(f"Error in adding user to group: {e}")
            return {'error': 'An unexpected error occurred while adding user to a  group.'}, 500 
        
@admin_ns_add.route('/group-permissions')
class Permissions(Resource):
    @admin_ns_add.expect(group_permission_model)
    @admin_ns_add.response(201, 'Permission created successfully')
    @admin_ns_add.response(400, 'Invalid input data')
    @admin_ns_add.response(500, 'Internal server error')
    def post(self): 
        try:
            from src.service.admin.admin_add_service import process_permission_service  # Import the utility function
            data = request.json
            print("group_permission_data",data)
            response, status_code = process_permission_service(data)
            return response, status_code
        except Exception as e:
            print(f"Error in adding permission: {e}")
            return {"error": "An error occurred"}, 500
        
@admin_ns_add.route('/user-permissions')
class Permissions(Resource):
    @admin_ns_add.expect(user_permission_model)
    @admin_ns_add.response(201, 'Permission created successfully')
    @admin_ns_add.response(400, 'Invalid input data')
    @admin_ns_add.response(500, 'Internal server error')
    def post(self): 
        try:
            from src.service.admin.admin_add_service import process_user_permission_service  # Import the utility function
            data = request.json
            print("user_permission",data)
            response, status_code = process_user_permission_service(data)
            return response, status_code
        except Exception as e:
            print(f"Error in adding  user permission: {e}")
            return {"error": "An error occurred"}, 500
        




@admin_ns_add.route('/update-group-email-pass')
class UpdateEmailPass(Resource):
    @admin_ns_add.expect('update_email_pass')
    @admin_ns_add.response(201, 'Permission created successfully')
    @admin_ns_add.response(400, 'Invalid input data')
    @admin_ns_add.response(500, 'Internal server error')
    def post(self): 
        try:
            from src.controller import db
            data = request.json
            group_name = data.get('group_name')
            source = data.get('source')
            database = data.get('database')
            table = data.get('table')
            view_email = data.get('view_email')
            view_pass = data.get('view_pass')

            query = text("""
                UPDATE groups_permissions_table
                SET view_email = :view_email, view_pass = :view_pass
                WHERE `group` = :group AND source = :source 
                AND databases_names = :database AND table_name = :table
            """)
            db.session.execute(
            query, 
            {"view_email": view_email, "view_pass": view_pass, "group": group_name, "source": source, "database": database, "table": table}
            )
            db.session.commit()

            return ({"success": True, "message": "Permissions updated successfully"}), 200

        except Exception as e:
            return ({"success": False, "error": str(e)}), 500


@admin_ns_add.route('/update-user-email-pass')
class UpdateEmailPass(Resource):
    @admin_ns_add.expect('update_email_pass')
    @admin_ns_add.response(201, 'Permission created successfully')
    @admin_ns_add.response(400, 'Invalid input data')
    @admin_ns_add.response(500, 'Internal server error')
    def post(self): 
        try:
            from src.controller import db
            data = request.json
            user_name = data.get('user_name')
            source = data.get('source')
            database = data.get('database')
            table = data.get('table')
            view_email = data.get('view_email')
            view_pass = data.get('view_pass')

            query = text("""
                UPDATE  user_permissions_table1
                SET view_email = :view_email, view_pass = :view_pass
                WHERE `username` = :username AND source = :source 
                AND databases_names = :database AND table_name = :table
            """)
            db.session.execute(
            query, 
            {"view_email": view_email, "view_pass": view_pass, "username": user_name, "source": source, "database": database, "table": table}
            )
            db.session.commit()

            return ({"success": True, "message": "Permissions updated successfully"}), 200

        except Exception as e:
            return ({"success": False, "error": str(e)}), 500

        