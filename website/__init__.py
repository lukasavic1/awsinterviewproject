from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_cognito_auth import CognitoAuthManager
from flask_cognito_auth import login_handler
from flask_cognito_auth import logout_handler
from flask_cognito_auth import callback_handler
from database_create import create_dynamodb
db = SQLAlchemy()
DB_NAME = "database.db"
table = create_dynamodb()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    app.config['COGNITO_REGION'] = "eu-central-1"
    app.config['COGNITO_USER_POOL_ID'] = "eu-central-1_ZjFCiZo8W"
    app.config['COGNITO_CLIENT_ID'] = "7urm6bpj0cb9aee2jp4qaafda1"
    app.config['COGNITO_DOMAIN'] = "http://localhost:5000/"
    app.config['COGNITO_REDIRECT_URI'] = "http://localhost:5000/"
    cognito = CognitoAuthManager(app)


    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    #login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        #return 1
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')