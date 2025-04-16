from werkzeug.security import generate_password_hash
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from settings import MAIL_PASSWORD,my_email,BaseURL
import re

def login_user_service(data):
    from src.util.auth_utils_auth import check_user_existence 
    from flask import session
    try:
        print("Received data:", data)
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {"error": "Username and password are required"}, 400
        user = check_user_existence(username, password)
        if user:
            # Extract user details safely
            user_id = getattr(user, 'id', None)
            user_role = getattr(user, 'role', None)
            user_name = getattr(user, 'username', None)
            print(user_id,user_role,user_name)

            # Store details in the session
            session['user_name'] = user_name
            session['role'] = user_role
            print("user role is",session.get('role'))
            session['user_id'] = user_id
            print("username is",session.get('user_name'))
            print("login sucessful")
            return {"message": "Login successful","user_id": user_id,"role": user_role}, 200
        else:
            # Invalid credentials
            print("invalid crenditials")
            return {"error": "Invalid credentials"}, 401
    except Exception as e:
        print("Error in login_user_service:", e)
        return {"error": "An error occurred during login"}, 500



def signup_user_service(data):
    from src.util.auth_utils_auth import check_user_existence_signup,check_mail_existence_signup
    flash_messages = None
    print(data)
    print("Entering into signup service")
    from src.util.auth_utils_auth import create_user_in_mysql, create_user_in_mongo
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    def validate_password(password):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$'
        if not re.match(pattern, password):
            return False, ("Password must be at least 6 characters long and include at least one uppercase letter, one lowercase letter, and one digit.")
        return True, None
    
    def validate_email(email):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@altimetrik\.com$'
        if not re.match(email_pattern, email):
            return False, "Email must be a valid email address ending with @altimetrik.com."
        return True, None
    original_pass=password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        user_exists = check_user_existence_signup(username=username)
        mail_exists=check_mail_existence_signup(mail=email)
        print(user_exists)
        if user_exists:
            return {"error": "User already exists"}, 409
        if mail_exists:
                return {"error": "Mail already exists"}, 409
        
        # Validate username, email, and password
        if not re.fullmatch(r"[A-Za-z]{5,}", username):
            return {"error": "Username must be at least 5 characters long and contain only alphabets."}, 400
        
        is_valid_email, email_error_message = validate_email(email)
        if not is_valid_email:
            return {"error": email_error_message}, 400 
        
        is_valid, error_message = validate_password(password)
        if not is_valid:
            print("Error message", error_message)
            return {"error": error_message}, 400
        
        # Create the invite token and link before sending the email
        token = generate_password_hash(email + str(datetime.now()), method='scrypt')
        invite_link = f"{BaseURL}/query-login?token={token}"
        print(f"Invite link: {invite_link}")

        # Send the email first
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        msg = MIMEText(f"""
        <html>
            <body>
                <p>Hello {username},</p>
                <p>You have been invited to join our platform. Below are your details:</p>
                <ul>
                    <li><b>Username:</b> {username}</li>
                    <li><b>Temporary Password:</b> {password}</li>
                </ul>
                <p><a href="{invite_link}">Click here to complete your login</a>.</p>
                <p>Regards,<br>The Team</p>
            </body>
        </html>
        """, "html")
        msg['subject'] = "Login link for query-panel"
        msg["from"] = my_email
        msg["to"] = email

        # Attempt to send the email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(my_email, MAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            print("Email sent successfully.")
            # Now create the user in MySQL and MongoDB after the email is successfully sent
            create_user_in_mysql(username, email, hashed_password, role,original_pass)
            create_user_in_mongo(username, email, hashed_password, role,original_pass)
            return {"message": "Signup successful! Invitation sent to email."}, 200
        except Exception as email_error:
            print(f"Failed to send email: {email_error}")
            return {"error": "Signup successful but failed to send email."}, 200
    except Exception as e:
        print("Error during signup:", e)
        return {"error": f"Error during signup: {str(e)}"}, 500


 