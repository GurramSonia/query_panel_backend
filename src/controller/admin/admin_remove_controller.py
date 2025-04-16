from flask_restx import Resource
from flask import  request
from src.controller.admin.admin_ns import admin_ns_remove
from src.controller.admin.admin_models import(remove_group,remove_user,remove_user_usermangement,remove_group_operation,remove_user_operation,add_user_operation)

@admin_ns_remove.route('/remove_user')
class RemoveUser(Resource):
    @admin_ns_remove.expect(remove_user)
    @admin_ns_remove.response(201, 'user is removed succesfully')
    @admin_ns_remove.response(400, 'Invalid input data')
    @admin_ns_remove.response(500, 'Internal server error')
    def post(self):
        try:
            from src.service.admin.admin_remove_service  import remove_user_service
            data = request.json
            group_name = data.get("group_name")
            username = data.get("username")
            print(group_name,username)
            if not group_name or not username:
                 return ({"error": "Missing group_name or username"}), 400
            response, status_code = remove_user_service(group_name,username)
            return response, status_code
        except Exception as e:
            print(f"Error in removing user from group: {e}")
            return {'error': 'An unexpected error occurred removing user from group.'}, 500 
        
@admin_ns_remove.route('/remove_group')
class RemoveUser(Resource):
    @admin_ns_remove.expect(remove_group)
    @admin_ns_remove.response(201, 'group is removed succesfully')
    @admin_ns_remove.response(400, 'Invalid input data')
    @admin_ns_remove.response(500, 'Internal server error')
    def post(self):
        try:
            from src.service.admin.admin_remove_service  import remove_group_service
            data = request.json
            group_name = data.get("group_name")
            print(group_name)
            if not group_name :
                 return ({"error": "Missing group_name"}), 400
            response, status_code = remove_group_service(group_name)
            return response, status_code
        except Exception as e:
            print(f"Error in removing user from group: {e}")
            return {'error': 'An unexpected error occurred removing user from group.'}, 500 

@admin_ns_remove.route('/remove-user-usermangement')
class RemoveUser(Resource):
    @admin_ns_remove.expect(remove_user_usermangement)
    @admin_ns_remove.response(201, 'user is removed succesfully')
    @admin_ns_remove.response(400, 'Invalid input data')
    @admin_ns_remove.response(500, 'Internal server error')
    def post(self):
        try:
            from src.service.admin.admin_remove_service  import remove_user_usermanagement_service
            data = request.json
            username = data.get("username")
            print(username)

            if not username:
                 return ({"error": "Missing  username"}), 400
            response, status_code = remove_user_usermanagement_service(username)
            return response, status_code
        except Exception as e:
            print(f"Error in removing user from usermanagement: {e}")
            return {'error': 'An unexpected error occurred removing user from group.'}, 500 

@admin_ns_remove.route('/group_operation_remove')
class RemoveUser(Resource):
    @admin_ns_remove.expect(remove_group_operation)
    @admin_ns_remove.response(201, 'group operation is removed succesfully')
    @admin_ns_remove.response(400, 'Invalid input data')
    @admin_ns_remove.response(500, 'Internal server error')
    def post(self):
        try:
            from src.service.admin.admin_remove_service  import remove_group_operation_service
            data = request.json
            group_name = data.get("group_name")
            source = data.get("source")
            database = data.get("database")
            table = data.get("table")
            operation = data.get("operation")
            if not all([group_name, source, database, table, operation]):
             return ({"error": "Missing required parameters"}), 400
            response, status_code = remove_group_operation_service(group_name,source,database,table,operation)
            return response, status_code
        except Exception as e:
            print(f"Error in removing operation from group: {e}")
            return {'error': 'An unexpected error occurred removing operation from group.'}, 500 
        
@admin_ns_remove.route('/user_operation_remove')
class RemoveUser(Resource):
    @admin_ns_remove.expect(remove_user_operation)
    @admin_ns_remove.response(201, 'user operation is removed succesfully')
    @admin_ns_remove.response(400, 'Invalid input data')
    @admin_ns_remove.response(500, 'Internal server error')
    def post(self):
        try:
            from src.service.admin.admin_remove_service  import remove_user_operation_service
            data = request.json
            user_name = data.get("user_name")
            source = data.get("source")
            database = data.get("database")
            table = data.get("table")
            operation = data.get("operation")
            if not all([user_name, source, database, table, operation]):
             return ({"error": "Missing required parameters"}), 400
            response, status_code = remove_user_operation_service(user_name,source,database,table,operation)
            return response, status_code
        except Exception as e:
            print(f"Error in removing operation from user: {e}")
            return {'error': 'An unexpected error occurred removing operation from user.'}, 500
        

