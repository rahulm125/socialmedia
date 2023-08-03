from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import configure_uploads, IMAGES, UploadSet
from config import Config


########################################### initializing flask app ###########################################
app = Flask(__name__)

########################################### get configurations ###########################################
app.config.from_object(Config)

##################################### initializing SQLAlchemy and Flask-Migrate #####################################
db = SQLAlchemy()
db.init_app(app)
Migrate(app, db)

########################################### uploadsets ###########################################
VIDEOS = ('mp4','mov','avi','flv','mkv','wmv')
images = UploadSet('images', IMAGES)
videos = UploadSet('videos', VIDEOS)


configure_uploads(app, (images, videos))

########################################### login manager ###########################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.signin"

########################################### importing blueprints ###########################################
from myapp.users.views import users_blueprint
from myapp.admin.views import admin_blueprint
from myapp.friends.views import friends_blueprint

########################################### registering blueprints ###########################################
app.register_blueprint(users_blueprint, url_prefix='/')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(friends_blueprint, url_prefix='/friends')










