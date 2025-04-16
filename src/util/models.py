from flask_login import  UserMixin
from datetime import datetime
from flask_login import  UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
db = SQLAlchemy()
mongo = PyMongo()

class MongoUser(UserMixin):
    def __init__(self, user_id, username,email, password, role):
        self.id = str(user_id)
        self.username = username
        self.email=email
        self.password = password
        self.role = role
    @property
    def is_active(self):
        return True
    @property
    def is_authenticated(self):
        return True if self.username else False
    @property
    def is_anonymous(self):
        return False
    
class User(db.Model, UserMixin): 
    __tablename__ = 'user'
     # Make sure UserMixin is included
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    originalpass = db.Column(db.String(255))

    def __repr__(self):
        return f'<User {self.username}>'
    def get_id(self):
        return str(self.id)  # Flask-Login expects string type ID
    @property
    def is_active(self):
        return True
        
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    database_name=db.Column(db.String(20), nullable=False)
    connection_string=db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 

def to_dict(self):
        """
        Convert the AuditLog instance into a dictionary with formatted timestamp.
        """
        return {
            'id': self.id,
            'username': self.username,
            'action': self.action,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime to string
        }

class Permission(db.Model):
    __tablename__ = 'groups_permissions_table'

    id = db.Column(db.Integer, primary_key=True)
    group=db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(50), nullable=False) 
    databases_names= db.Column(db.String(50), nullable=False) # e.g., MySQL, MongoDB
    table_name = db.Column(db.String(255), nullable=False)
    operations = db.Column(db.String(255), nullable=False)  # Comma-separated list of operations
    view_email = db.Column(db.Boolean, default=False, nullable=False)  # New column for email visibility
    view_pass = db.Column(db.Boolean, default=False, nullable=False) # Comma-separated list of operations


    def __repr__(self):
        return f"<Permission(group={self.group}, source={self.source},databases_names={self.databases_names}, table_name={self.table_name} view_email={self.view_email}, view_pass={self.view_pass})>"
    
class UserPermission(db.Model):
    __tablename__ = 'user_permissions_table1'

    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(50), nullable=False) 
    databases_names= db.Column(db.String(50), nullable=False) # e.g., MySQL, MongoDB
    table_name = db.Column(db.String(255), nullable=False)
    operations = db.Column(db.String(255), nullable=False) 
    view_email = db.Column(db.Boolean, default=False, nullable=False)  # New column for email visibility
    view_pass = db.Column(db.Boolean, default=False, nullable=False) # Comma-separated list of operations

    def __repr__(self):
        return f"<Permission(username={self.group}, source={self.source},databases_names={self.databases_names}, table_name={self.table_name},view_email={self.view_email}, view_pass={self.view_pass})>"

class Group(db.Model):
    __tablename__ = 'groups_names'  # Use a standard name without special characters

    id = db.Column(db.Integer, primary_key=True)  # Unique group ID
    group_name = db.Column(db.String(120), unique=True, nullable=False) 
    users = db.Column(db.String(120), unique=True, nullable=False )# Name of the group
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)



    def __repr__(self):
        return f'<Group {self.group_name}>'

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('reset_tokens', lazy=True))
    
    def __repr__(self):
        return f'<PasswordResetToken {self.token}>'

def create_tables():
    db.create_all()