# will make thw folder- website a python package 
# This file is used to initialize the Flask application and set up the database connection.
from flask import Flask # IMPORT Flask class from the flask package 
from flask_sqlalchemy import SQLAlchemy # IMPORT SQLAlchemy class from the flask_sqlalchemy package
from os import path #IMPORT path function from the os module THAT HANDLES file paths 
from flask_login import LoginManager # IMPORT LoginManager class from the flask_login package FOR user authentication and session management
# from .views import views 
# from .auth import auth

db = SQLAlchemy() # creates an instance of SQLAlchemy, which is used to interact with the database
DB_NAME = 'database.db' # This variable holds the name of the database file that will be created in the project directory

def create_app(): # This function creates and configures the Flask application
    # This function initializes the Flask application, sets up the database, and registers blueprints for routing.
    print("Flask app initialized...")
    app = Flask(__name__) # creates an instance of the Flask class, which is the main application object 
    app.config['SECRET_KEY'] = "12345678" # secure the cookies and session data related to our app (encrpts it )
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) # initializes the SQLAlchemy instance with the Flask app, allowing it to interact with the database
    # tell the app that there are urls 
    from .views import views 
    from .auth import auth
    # Register the routes with the flask app
    app.register_blueprint(views, url_prefix='/')# maps '/' to the views blueprint
    app.register_blueprint(auth, url_prefix='/') # maps '/' to the auth blueprint
    # This allows the application to handle requests for both the views and auth blueprints.

    # Database creation 
    from .models import User, Note

    create_database(app)# creates the database if it does not exist

    login_manager = LoginManager() # creates an instance of the LoginManager class, which is used for user authentication and session management
    login_manager.login_view = 'auth.login' # This specifies the view to redirect to when a user tries to access a protected route without being logged in
    login_manager.init_app(app) # initializes the LoginManager instance with the Flask app, allowing it to manage user sessions

    # This function is called to load the user from the database based on the user ID stored in the session.
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
     
    return app # This returns the configured Flask application instance, which can be used to run the app or handle requests.

def create_database(app):
    if not path.exists('website/' + DB_NAME): # checks if the database file does not exist
        with app.app_context(): # creates an application context for the Flask app
            db.create_all() # creates the database and all the tables defined in the models
            print('Created Database!')  


# Above we have created and initialized a Flask applicationn 