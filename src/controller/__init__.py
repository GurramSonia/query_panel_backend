from flask import Blueprint,url_for,Flask
import os
from flask_mail import Mail
from flask_restx import Api,apidoc
from src.controller.auth.auth_controller_auth import auth_ns_auth
from src.controller.auth.auth_controller_reset_pass import auth_ns_reset_pass
from src.controller.admin.admin_get_controller import admin_ns_get 
from src.controller.admin.admin_add_controller import admin_ns_add
from src.controller.admin.admin_remove_controller import admin_ns_remove
from src.controller.query_connection_controller import connection_ns
from src.util.models import db, mongo
from settings import MYSQL_USER,MYSQL_DATABASE,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_PORT,MONGO_USERNAME,MONGO_PASSWORD,MONGO_DATABASE,MONGO_HOST,MONGO_PORT

mail = Mail()
class MyCustomApi(Api):
    def _register_apidoc(self, app: Flask) -> None:
        conf = app.extensions.setdefault('restx', {})  # Use 'restx' instead of 'restplus'
        custom_apidoc = apidoc.Apidoc('restx_doc', 'flask_restx.apidoc',  # Use 'flask_restx' instead of 'flask_restplus'
                                      template_folder='templates', static_folder='static',
                                      static_url_path='/queryapi')

        @custom_apidoc.add_app_template_global
        def swagger_static(filename: str) -> str:
            return url_for('restx_doc.static', filename=filename)  # Use 'restx_doc' instead of 'restplus_doc'

        if not conf.get('apidoc_registered', False):
            app.register_blueprint(custom_apidoc)
            conf['apidoc_registered'] = True

queryapi= Blueprint('my_blueprint', __name__, url_prefix='/queryapi')
""" API = MyCustomApi(queryapi, version='1.0', title='QueryPanel API', description='API Querypanel',
                  validate=True) """
API = Api(queryapi, version='1.0', title='QueryPanel-APP-API', description='API Querypanel',
                  validate=True) 
 

def init_app(app):
    MYSQL_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST and MYSQL_DATABASE
        else 'mysql+pymysql://GurramSonia:Ramya772819390@localhost/querydatabase2'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # MongoDB configuration
    MONGO_URI = (
        f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}"
        if MONGO_USERNAME and MONGO_PASSWORD and MONGO_HOST and MONGO_DATABASE
        else 'mongodb://localhost:27017/mongo-database'
    )
    app.config['MONGO_URI'] = MONGO_URI
    app.config['SECRET_KEY'] = 'my_app_secret_it_is_confidential'

    db.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)

    # Register namespaces with the API
    API.add_namespace(auth_ns_auth, path='/auth')
    API.add_namespace(auth_ns_reset_pass, path='/auth')
    API.add_namespace(admin_ns_add, path='/admin')
    API.add_namespace(admin_ns_get, path='/admin')
    API.add_namespace(admin_ns_remove, path='/admin')
    API.add_namespace(connection_ns, path='/connection/')

    # Register the Blueprint with the app
    app.register_blueprint(queryapi)

    # Create database tables
    with app.app_context():
        db.create_all()
