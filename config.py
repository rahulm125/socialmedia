import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-can-never-guess-my-key-rahul-muthe'
    SQLALCHEMY_DATABASE_URI = 'mysql://socialmedia:socialmedia@localhost/socialmedia'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_IMAGES_DEST = 'myapp/static/uploads/images'
    UPLOADED_VIDEOS_DEST = 'myapp/static/uploads/videos'
    USERS_PER_TABLE = 3
