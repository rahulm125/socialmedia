from flask import Blueprint, render_template, redirect, flash, url_for, request, session
from myapp import db
from flask_login import login_user, login_required, logout_user
from myapp.models import User, FriendsList, FriendsReq, FriendsPen
from myapp.friends.forms import AddFriend


friends_blueprint = Blueprint('friends', __name__, template_folder='templates/friends')

@friends_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def friends():
    user = session['user']
    user_info = User.query.filter_by(username=user).first()
    frnd_lst = FriendsList.query.filter_by(user_id=user_info.id).all()
    req_lst = FriendsReq.query.filter_by(user_id=user_info.id).all()
    pen_lst = FriendsPen.query.filter_by(user_id=user_info.id).all()


    return render_template('friends.html', frnd_lst=frnd_lst, req_lst=req_lst, pen_lst=pen_lst)

@friends_blueprint.route('/addfriend', methods=['GET', 'POST'])
@login_required
def addfriend():
    form = AddFriend()
    users = session['user']
    user = db.session.query(User.id).filter(User.username == users).first()
    uid  = user.id

    friends = User.query.all()
    form.friends.choices = [(friends.id) for friends in friends]
    if form.validate_on_submit():
        rid = form.friends.data

        addreq = FriendsReq(user_id=rid, req_id=uid)
        addpen = FriendsPen(user_id=uid, pen_id=rid)
        db.session.add(addreq)
        db.session.add(addpen)
        db.session.commit()
        return render_template("addfrnd.html", users=users, form=form)

    return render_template("addfrnd.html", form=form, friends=friends)
