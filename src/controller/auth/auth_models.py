
from flask_restx import fields
from src.controller.auth.auth_ns import auth_ns_auth,auth_ns_reset_pass

login_model = auth_ns_auth.model('LoginModel', {
        'username': fields.String(required=True, description='Username for login',example='test_user'),
        'password': fields.String(required=True, description='Password for login',password='testpass123')
})

signup_model = auth_ns_auth.model('SignupModel', {
        'username': fields.String(required=True, description='New user username'),
        'email': fields.String(required=True, description='New user email'),
        'password': fields.String(required=True, description='New user password'),
        'role': fields.String(required=True, description='role')
}) 

current_user_model = auth_ns_auth.model('CurrentUserModel', {
        'username': fields.String(description='Logged-in user\'s username'),
        'email': fields.String(description='Logged-in user\'s email'),
        'role': fields.String(description='Logged-in user\'s role')
})

reset_password_model=auth_ns_reset_pass.model('CurrentUserModel', {
        'newPassword':fields.String(description='NewPassword'),
   
})
forgot_pass_model = auth_ns_reset_pass.model('ForgotModel', {
        'email': fields.String(required=True, description='emai for reset',password='username@gmail.com')
})