from flask import  request, jsonify, session
from flask_restx import Resource
from src.controller.auth.auth_ns import auth_ns_auth
from src.controller.auth.auth_models import (login_model,signup_model,current_user_model)

@auth_ns_auth.route('/current_user')
class CurrentUser(Resource):
    @auth_ns_auth.response(200, 'Got current user details')
    @auth_ns_auth.response(401, 'Unauthorized')
    @auth_ns_auth.response(404, 'User not found')
    def get(self):
        try:
            from src.util.auth_utils_auth import get_user_details_by_id
            user_id = session.get('user_id')  
            print("entered into current users")
            if not user_id:
                return ({"error": "Unauthorized"}), 401
            user_details = get_user_details_by_id(user_id)
            print(user_details)
            if not user_details:
                return ({"error": "User not found"}), 404
            return {"username": user_details['username'],  "email": user_details['email'],"role": user_details['role']}, 200
        except Exception as e:
            print(f"Error fetching current user details: {e}")
            return ({"error": "An error occurred"}), 500

@auth_ns_auth.route('/query-login')
class Login(Resource):
    @auth_ns_auth.expect(login_model)
    @auth_ns_auth.response(200, 'Login successful')
    @auth_ns_auth.response(400, 'Invalid JSON')
    @auth_ns_auth.response(500, 'Server error')
    def post(self):
        print("entered into login")
        from src.service.auth_service import login_user_service
        try:
            data = request.get_json()
            print(f"Received login data: {data}")
            if not data:
                return {"error": "Invalid JSON"}, 400
            response = login_user_service(data)
            print("Response received:", response)
            return response
        except Exception as e:
            print("Error in login route:", e)
            return {"error": "An error occurred"}, 500
        
@auth_ns_auth.route('/query-signup')
class Signup(Resource):
    @auth_ns_auth.expect(signup_model)
    @auth_ns_auth.response(201, 'User created successfully')
    @auth_ns_auth.response(400, 'Validation error')
    @auth_ns_auth.response(500, 'Server error')
    def post(self):
        from src.service.auth_service import signup_user_service
        try:
             print("entered into signup")
             data = request.json
             print(data)
             response= signup_user_service(data)
             print("respose is",response)
             return response ,201
        except Exception as e:
            print(f"Error in signup route: {e}")
            return ({"error": "An error occurred during signup"}), 500