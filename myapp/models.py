from myapp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

########################################### login manager ###########################################
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

########################################### user data table ###########################################
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True, index=True)
    dob = db.Column(db.String(100))
    username = db.Column(db.String(60), unique=True, index=True)
    gender = db.Column(db.String(50))
    authenticated = db.Column(db.Boolean, default=False, nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.now)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Boolean, default=False, nullable=False)
    desc = db.Column(db.String(300))
    facebook = db.Column(db.String(300))
    instagram = db.Column(db.String(300))

    ########################################### defining user table relationships #####################################
    frnd_id = db.relationship('FriendsList', backref='user', lazy='dynamic')
    f_id = db.relationship('FollowList', backref='user', lazy='dynamic')
    req_id = db.relationship('FriendsReq', backref='user', lazy='dynamic')
    pen_id = db.relationship('FriendsPen', backref='user', lazy='dynamic')
    pp_id = db.relationship('ProfilePhotos', backref='user', lazy='dynamic')
    cc_id = db.relationship('CoverPhotos', backref='user', lazy='dynamic')
    post_id = db.relationship('Posts', backref='user', lazy='dynamic')
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='user', lazy='dynamic')
    comments = db.relationship('PostComment', foreign_keys='PostComment.user_id', backref='user', lazy='dynamic')


    ########################################### initializing class ###########################################
    def __init__(self, firstname, lastname, email, dob, username, gender, authenticated, password, role,
                 desc, facebook, instagram):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.dob = dob
        self.username = username
        self.gender = gender
        self.authenticated = authenticated
        self.password_hash = generate_password_hash(password)  # hashed the password
        self.role = role
        self.desc = desc
        self.facebook = facebook
        self.instagram = instagram

    ########################################### function to add like post ###########################################
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    ########################################### function to unlike post ###########################################
    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    ########################################### function to check if like post ########################################
    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    ########################################### function to check password ###########################################
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    ############################ function to check if user is authenticated by admin ##################################
    def is_active(self):
        if self.authenticated:
            return True
        return False

    ################################### function to check if user is admin ##########################################
    def is_admin(self):
        if self.role:
            return True
        else:
            return False

    ################################### function to check if user is friend ########################################
    def is_friend(self, res):
        for frnd in res:
            if self.id == frnd.frnd_id:
                return True


################################### Table to store friends of user ########################################
class FriendsList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frnd_id = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self, frnd_id, user_id):
        self.frnd_id = frnd_id
        self.user_id = user_id


################################### Table to store received friend requests ########################################
class FriendsReq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    req_id = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self, req_id, user_id):
        self.req_id = req_id
        self.user_id = user_id

################################### Table to store sent friend requests ########################################
class FriendsPen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pen_id = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self, pen_id, user_id):
        self.pen_id = pen_id
        self.user_id = user_id

################################### Table to store layout data ########################################
class WebSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    favicon = db.Column(db.String(300))
    logo = db.Column(db.String(300))
    copyrights = db.Column(db.String(300))
    lsliderone = db.Column(db.String(300))
    lonedesc = db.Column(db.String(300))
    lonephoto = db.Column(db.String(300))
    lslidertwo = db.Column(db.String(300))
    ltwodesc = db.Column(db.String(300))
    ltwophoto = db.Column(db.String(300))
    lsliderthree = db.Column(db.String(300))
    lthreedesc = db.Column(db.String(300))
    lthreephoto = db.Column(db.String(300))
    swebheading = db.Column(db.String(300))
    sdesc = db.Column(db.String(300))
    lphoto = db.Column(db.String(300))
    signup = db.Column(db.Boolean, default=True, nullable=False)


    def __init__(self, name, favicon, logo, copyrights, lsliderone, lonedesc, lonephoto, lslidertwo, ltwodesc, ltwophoto,
                 lsliderthree, lthreedesc, lthreephoto, swebheading, sdesc, lphoto, signup):

        self.name = name
        self.favicon = favicon,
        self.logo = logo
        self.copyrights = copyrights
        self.lsliderone = lsliderone
        self.lonedesc = lonedesc
        self.lonephoto = lonephoto
        self.lslidertwo = lslidertwo
        self.ltwodesc = ltwodesc
        self.ltwophoto = ltwophoto
        self.lsliderthree = lsliderthree
        self.lthreedesc = lthreedesc
        self.lthreephoto = lthreephoto
        self.swebheading = swebheading
        self.sdesc = sdesc
        self.lphoto = lphoto
        self.signup = signup


################################### Table to store follow list of user ########################################
class FollowList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_id = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self, f_id, user_id):
        self.f_id = f_id
        self.user_id = user_id

################################### Table to store cover photos of user ########################################
class CoverPhotos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cover = db.Column(db.String(300))
    current = db.Column(db.Boolean, default=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self,cover, user_id, current):
        self.cover = cover
        self.user_id = user_id
        self.current = current

################################### Table to store profile photos of user ########################################
class ProfilePhotos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.String(300))
    current = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def __init__(self, profile, user_id, current):
        self.profile = profile
        self.user_id = user_id
        self.current = current

################################### Table to store user Posts ########################################
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    desc = db.Column(db.String(300))
    type = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    name = db.Column(db.String(200))
    filetype = db.Column(db.String(200))
    profilephoto = db.Column(db.String(300))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    comments = db.relationship('PostComment', backref='post', lazy='dynamic')

    def __init__(self, filename, desc, type, user_id, name, filetype, profilephoto):
        self.filename = filename
        self.desc = desc
        self.type = type
        self.user_id = user_id
        self.name = name
        self.filetype = filetype
        self.profilephoto = profilephoto

    ################################### function to get comments of post ########################################
    def get_comments(self):
        return PostComment.query.filter_by(post_id=self.id).order_by(PostComment.timestamp.desc())

################################### Table to store like of posts ########################################
class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id

################################### Table to store comments of posts ########################################
class PostComment(db.Model):
    __tablename__ = 'post_comment'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200))
    name = db.Column(db.String(200))
    photo = db.Column(db.String(200))
    time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, comment, name, photo, user_id, post_id):
        self.comment = comment
        self.name = name
        self.photo = photo
        self.user_id = user_id
        self.post_id = post_id

    ################################### function to get user who has commented ########################################
    def get_user(self):
        return User.query.filter_by(id=self.user_id).first()
        
