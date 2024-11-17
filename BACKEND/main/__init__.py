import os  
import logging  
from flask import Blueprint, Flask, app  
from dotenv import load_dotenv  
from flask_restful import Api  
from flask_sqlalchemy import SQLAlchemy  
from flask_jwt_extended import JWTManager  
from flask_mail import Mail  
from flask_cors import CORS 
# Configuración del logging  
logging.basicConfig(level=logging.INFO)  

# Inicializar las extensiones de Flask  
api = Api()  
db = SQLAlchemy()  
jwt = JWTManager()  
mailsender = Mail()  

def create_app():  
    app = Flask(__name__)
    load_dotenv()
    
    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)


    # Database setup  
    database_path = os.path.join(os.getenv('DATABASE_PATH'), os.getenv('DATABASE_NAME'))  
    if not os.path.exists(database_path):  
        os.mknod(database_path)  

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path  
    db.init_app(app)  

    # Load resources into API  
    import main.resources as resources  
    api.add_resource(resources.PoemsResource, '/poems')  
    api.add_resource(resources.UsersResource, '/users')  
    api.add_resource(resources.ReviewsResource, '/reviews')  
    api.add_resource(resources.PoemResource, '/poem/<id>')  
    api.add_resource(resources.UserResource, '/user/<id>')  
    api.add_resource(resources.ReviewResource, '/review/<id>')  
    api.init_app(app)  

    # JWT configuration  
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))  
    jwt.init_app(app)  

    from main.auth import routes  
    app.register_blueprint(routes.auth)  

    # Mail configuration  
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')  
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')  
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')  
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')  
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')  
    mailsender.init_app(app) 
    return app 

