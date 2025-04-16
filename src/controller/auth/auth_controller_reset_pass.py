from flask import  request
from flask_restx import Resource
import smtplib
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash
import smtplib
from email.mime.text import MIMEText
from settings import MAIL_PASSWORD,my_email,BaseURL
from src.util.auth_utils_reset_pass import get_user_by_token, reset_user_password
from src.controller.auth.auth_ns import auth_ns_reset_pass
from src.controller.auth.auth_models import (forgot_pass_model,reset_password_model)

@auth_ns_reset_pass.route('/forgot-password')
class ForgotPassword(Resource):
    @auth_ns_reset_pass.expect(forgot_pass_model)  # Ensure this model validates the email input
    @auth_ns_reset_pass.response(200, 'Password reset link sent')
    @auth_ns_reset_pass.response(404, 'Email not found')
    @auth_ns_reset_pass.response(500, 'Server error')
    def post(self):
        from src.util.auth_utils_reset_pass import check_user_existence_by_email,generate_reset_token
        email = request.json.get('email')
        user = check_user_existence_by_email(email)
        if not user:
            return {"error": "Email not found"}, 404
        reset_token = generate_reset_token(email)  # Call a function to generate and save token
        reset_link = f"{BaseURL}/reset-password?token={reset_token}"
        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            msg = MIMEText(f"""
            <html>
                <body>
                    <p>Hello,</p>
                    <p>To reset your password, please click the following link:</p>
                    <p><a href="{reset_link}">Reset Password</a></p>
                </body>
            </html>
            """, "html")
            msg['Subject'] = "Password Reset Request"  
            msg['From'] = my_email
            msg['To'] = email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(my_email, MAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            return {"message": "Password reset link sent to your email."}, 200
        except Exception as e:
            print(f"Email sending failed: {e}")
            return {"error": "Failed to send email. Please try again."}, 500
        
@auth_ns_reset_pass.route('/reset-password')
class ResetPassword(Resource):
    @auth_ns_reset_pass.expect(reset_password_model) 
    @auth_ns_reset_pass.response(200, 'Password reset successful')
    @auth_ns_reset_pass.response(400, 'Invalid token or missing password')
    @auth_ns_reset_pass.response(500, 'Server error')
    def post(self):
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('newPassword')
        password=new_password
        if not token or not new_password:
            return {'error': 'Token and new password are required'}, 400
        user = get_user_by_token(token)
        if not user:
            return {'error': 'Invalid or expired token'}, 400
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        mongo_username=user.username
        try:
            reset_user_password(user.id, hashed_password,mongo_username,password)
            return {'message': 'Password reset successfully'}, 200
        except Exception as e:
            return {'error': f'Failed to reset password: {str(e)}'}, 500
