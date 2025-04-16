from flask_restx import  Resource
from flask import session,request
from src.controller.admin.admin_ns import admin_ns_get
from src.controller.admin.admin_models import(operations)

@admin_ns_get.route('/available_databases')
class AvailableDatabases(Resource):
    @admin_ns_get.response(200, 'Got available databases', as_list=True)
    @admin_ns_get.response(401, 'Unauthorized')
    def get(self):
        try:
            from src.service.admin.admin_get_service import get_available_databases_service  # Import the utility function
            role=session.get('role')
            print("user role in available databases is",role)
            username = session.get('user_name')
            print("Username is:", username)
            response, status_code = get_available_databases_service(username)
            print(response)
            return response, status_code
        except Exception as e:
            print(f"Error fetching available databases: {e}")
            return {'error': 'An error occurred while fetching databases'}, 500

@admin_ns_get.route('/available_connections')
class AvailableDatabases(Resource):
    @admin_ns_get.response(200, 'Got available databases', as_list=True)
    @admin_ns_get.response(401, 'Unauthorized')
    def post(self):
        try:
            from src.service.admin.admin_get_service import get_available_connections_service  # Import the utility function
            role=session.get('role')
            data = request.json
            database = data.get('database')
            print("user role in available databases is",role)
            username = session.get('user_name')
            print("Username is:", username)
            response, status_code = get_available_connections_service(username,database)
            print(response)
            return response, status_code
        except Exception as e:
            print(f"Error fetching available databases: {e}")
            return {'error': 'An error occurred while fetching databases'}, 500
        
@admin_ns_get.route('/available_databases_names')
class AvailableDatabases(Resource):
    @admin_ns_get.response(200, 'Got available databases', as_list=True)
    @admin_ns_get.response(401, 'Unauthorized')
    def post(self):
        try:
            from src.service.admin.admin_get_service import get_available_databases_names_service  # Import the utility function
            role=session.get('role')
            data = request.json
            database = data.get('database')
            print("user role in available databases is",role)
            username = session.get('user_name')
            print("Username is:", username)
            response, status_code = get_available_databases_names_service(username,database)
            print(response)
            return response, status_code
        except Exception as e:
            print(f"Error fetching available databases: {e}")
            return {'error': 'An error occurred while fetching databases'}, 500
    
@admin_ns_get.route('/audit_logs')
class AuditLogs(Resource):
    @admin_ns_get.response(200, 'Got audit_logs',as_list=True)
    @admin_ns_get.response(401, 'Unauthorized')
    def get(self):
        print("entered into audit_logs")
        try:
             from src.service.admin.admin_get_service import fetch_audit_logs_service # Import the utility function
             print("Entered into audit_logs")
             response, status_code = fetch_audit_logs_service()
             return response, status_code
        except Exception as e:
            return {'error': str(e)}, 500

@admin_ns_get.route('/users')
class Users(Resource):
    @admin_ns_get.response(200, 'users',as_list=True)
    @admin_ns_get.response(401, 'Unauthorized')
    def get(self):
        print("Entered into users endpoint")
        try:
            from src.util.models import db
            from src.service.admin.admin_get_service import fetch_users_service  # Import the utility function
            response, status_code = fetch_users_service(db)
            return response, status_code
        except Exception as e:
            print(f"Error fetching users: {e}")
            return {'error': 'An error occurred while fetching users'}, 500
        
@admin_ns_get.route('/groups')
class Users(Resource):
    @admin_ns_get.response(200, 'groups',as_list=True)
    @admin_ns_get.response(401, 'Unauthorized')
    def get(self):
        print("Entered into users endpoint")
        try:
            from src.util.models import db
            from src.service.admin.admin_get_service import fetch_groups_service  # Import the utility function
            response, status_code = fetch_groups_service(db)
            return response, status_code
        except Exception as e:
            print(f"Error fetching users: {e}")
            return {'error': 'An error occurred while fetching users'}, 500
        
@admin_ns_get.route('/user-operations')
class GetUserOperations(Resource):
    @admin_ns_get.response(201, 'user-operations successfully accessed')
    @admin_ns_get.response(400, 'Invalid input data')
    @admin_ns_get.response(500, 'Internal server error')
    def get(self):
        try:
            from src.service.admin.admin_get_service import get_user_operations
            response, status_code = get_user_operations()
            return response, status_code
        except Exception as e:
            print(f"Error in getting  user-operations: {e}")
            return {'error': 'An unexpected error occurred while getting operations.'}, 500 
        
@admin_ns_get.route('/group-operations')
class GetOperations(Resource):
    @admin_ns_get.response(201, 'operations successfully accessed')
    @admin_ns_get.response(400, 'Invalid input data')
    @admin_ns_get.response(500, 'Internal server error')
    def get(self):
        try:
            from src.service.admin.admin_get_service import get_group_operations
            response, status_code = get_group_operations()
            return response, status_code
        except Exception as e:
            print(f"Error in getting operations: {e}")
            return {'error': 'An unexpected error occurred while getting operations.'}, 500 
