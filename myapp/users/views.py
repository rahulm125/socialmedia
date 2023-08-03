from flask import Blueprint, render_template, redirect, flash, url_for, request, session
from myapp import db, images, videos, IMAGES, VIDEOS, app
from flask_login import login_user, login_required, logout_user, current_user
from myapp.models import User, WebSettings, FriendsList, FriendsReq, FriendsPen, FollowList,\
    ProfilePhotos, CoverPhotos, Posts, PostComment
from myapp.users.forms import SignUpForm, years, SignInForm, NewPostForm, BasicProfileForm, SearchForm, CommentForm
from sqlalchemy.sql import func
from flask_sqlalchemy import Pagination


################################### declaring user blueprint ########################################
users_blueprint = Blueprint('users', __name__, template_folder='templates/users')


################################### route and function for user signup ########################################
@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():

    snumb = "1234567890"

    special_character = "1234567890"

    def is_valid(username):
        global special_character
        return any(char in snumb for char in username)

    details = WebSettings.query.all()
    form = SignUpForm()
    year = years(1950,2022)
    month = [('January'), ('Febuary'), ('March'), ('April'), ('May'), ('June'), ('July'),
                                          ('August'), ('September'), ('October'), ('November'), ('December')]

    if form.validate_on_submit():
        if request.method == 'POST':
            email = User.query.filter_by(email=form.email.data).first()
            if email is None:
                username = User.query.filter_by(username=form.username.data).first()
                if username is None:
                    if is_valid(form.username.data):
                        date = str(form.date.data)

                        byear = str(request.form.get('dyear'))
                        bmonth = request.form.get('dmonth')

                        dob = date+'/'+bmonth+'/'+byear

                        authenticated = False
                        desc = "Your Description Here"
                        # photo = "user.jpg"
                        # cover = "cover.jpg"
                        facebook = 'Facebook Profile'
                        instagram = 'Instagram Profile'

                        register = User(firstname=form.firstname.data, lastname=form.lastname.data,
                                        email=form.email.data, username=form.username.data, password=form.password.data,
                                        dob=dob, gender=form.gender.data, authenticated=authenticated,
                                        role=False, desc=desc, facebook=facebook, instagram=instagram)
                        db.session.add(register)
                        db.session.commit()
                        flash('Account Created Successfully')

                        return redirect(url_for('users.signin'))
                    else:
                        flash('Username must contain at least one number')
                        return redirect(url_for('users.signup'))
                else:
                    flash('Username already exists, please try again!')
                    return redirect(url_for('users.signin'))
            else:
                flash('Email already exists, please try logging in!')
                return redirect(url_for('users.signin'))

    return render_template('signup.html', form=form, year=year, month=month, details=details)


################################### route and function for user signin ########################################
@users_blueprint.route('', methods=['GET', 'POST'])
def signin():
    details = WebSettings.query.all()
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                session['user'] = form.username.data
                status = user.is_active()
                if status:
                    login_user(user)
                    next = request.args.get('next')
                    if next == None or not next[0] == '/':
                        next = url_for('users.feed')
                    return redirect(next)
                else:
                    flash('Be patient! Your account is being verified')
                    fullname = user.firstname+" "+user.lastname
                    return redirect(url_for('users.signin', fullname=fullname))

            else:
                flash('Wrong Password')
                return redirect(url_for('users.signin'))

        else:
            flash('Username not found')
            return redirect(url_for('users.signin'))
    return render_template('signin.html', form=form, details=details)


################################### route and function for thankyou page ########################################
@users_blueprint.route('/thankyou/<string:fullname>')
@login_required
def thankyou(fullname):
    return "Thank You"+ fullname

################################### route and function for logout ########################################
@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.signin'))


################################### route and function for user profile(self) ########################################
@users_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    pagename = 'User Profile'
    details = WebSettings.query.all()
    user = current_user.username
    user_info = User.query.filter_by(username=current_user.username).first()
    profilepic = ProfilePhotos.query.filter_by(current=True, user_id=user_info.id).first()
    coverpic = CoverPhotos.query.filter_by(current=True, user_id=user_info.id).first()
    friends = FriendsList.query.filter_by(user_id=user_info.id).all()
    following = FollowList.query.filter_by(user_id=user_info.id).all()
    followers = FollowList.query.filter_by(f_id=user_info.id).all()
    follow_lst = FollowList.query.filter_by(user_id=user_info.id).all()
    posts = Posts.query.filter_by(user_id=user_info.id).all()
    friend_suggestions = User.query.filter(User.username != user).order_by(func.rand()).limit(11)
    newform = NewPostForm()
    if newform.validate_on_submit():
        name = user_info.firstname + ' ' + user_info.lastname
        if newform.files.data:
            fileis = newform.files.data
            fname = fileis.filename
            valu = fname.split('.')
            a = []
            b = []
            for i in IMAGES:
                a.append(i)
            for j in VIDEOS:
                b.append(j)

            if valu[1] in a:
                filename = images.save(newform.files.data)
                desc = newform.desc.data
                ptype = newform.ptype.data
                filetype = 'image'
                newpost = Posts(filename=filename, desc=desc, type=ptype, user_id=user_info.id, name=name,
                                filetype=filetype, profilephoto=profilepic.profile)
                db.session.add(newpost)
                db.session.commit()
                return redirect(url_for('users.profile'))

            elif valu[1] in b:
                filename = videos.save(newform.files.data)
                desc = newform.desc.data
                ptype = newform.ptype.data
                filetype = 'video'
                newpost = Posts(filename=filename, desc=desc, type=ptype, user_id=user_info.id, name=name,
                                filetype=filetype, profilephoto=profilepic.profile)
                db.session.add(newpost)
                db.session.commit()
                redirect(url_for('users.profile'))
        else:
            filename = 'Null'
            desc = newform.desc.data
            ptype = newform.ptype.data
            filetype = 'simple'
            newpost = Posts(filename=filename, desc=desc, type=ptype, user_id=user_info.id, name=name,
                            filetype=filetype, profilephoto=profilepic.profile)
            db.session.add(newpost)
            db.session.commit()
            redirect(url_for('users.profile'))

        #############for showing posts###############
    cform = CommentForm()
    viewposts = []
    videoposts = []
    for p in posts:
        viewposts.append(p)
    for v in posts:
        if v.filetype == "video":
            videoposts.append(v)


    def get_profilepic(res):
        profile = ProfilePhotos.query.filter_by(current=True, user_id=res.id).first()
        if profile:
            return profile.profile

            ############### for checking if user followed ##############
    def is_follow(res, follow_lst):
         status = False
         for req in follow_lst:
            if res.id == req.f_id:
                status = True
         return status

    searchform = SearchForm()
    if searchform.validate_on_submit():
        search = searchform.search.data
        return redirect(url_for('users.search', search=search))
    return render_template("profile.html", newform=newform, user_info=user_info, details=details,
                           pagename=pagename, searchform=searchform, profilepic=profilepic, coverpic=coverpic,
                           friends=len(friends), followers=len(followers), following=len(following), posts=len(posts),
                           allposts=reversed(viewposts), videos=reversed(videoposts), cform=cform,
                           fsuggestions=friend_suggestions, profil=get_profilepic, is_follow=is_follow,
                           follow_lst=follow_lst)


################################### route and function for user settings ########################################
@users_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    pagename = 'User Settings'
    details = WebSettings.query.all()
    user = current_user.username
    user_id = db.session.query(User.id).filter(User.username == user).first()
    user_info = User.query.filter_by(username=user).one()
    profilepic = ProfilePhotos.query.filter_by(current=True, user_id=user_info.id).first()
    pphoto = ProfilePhotos.query.filter_by(user_id=user_info.id, current=True).first()
    cphoto = CoverPhotos.query.filter_by(user_id=user_info.id, current=True).first()
    followers = len(FollowList.query.filter_by(f_id=user_info.id).all())
    form = BasicProfileForm(obj=user_info)
    if form.validate_on_submit():
        user_info = User.query.get(user_id)
        form.populate_obj(user_info)
        if form.profile.data:
            prophoto = images.save(form.profile.data)
            if pphoto is not None:
                pphoto.current = False
                addphoto = ProfilePhotos(profile=prophoto, user_id=user_info.id, current=True)
                db.session.add(addphoto)
            else:
                addphoto = ProfilePhotos(profile=prophoto, user_id=user_info.id, current=True)
                db.session.add(addphoto)
        if form.cover.data:
            coverphoto = images.save(form.cover.data)
            if cphoto is not None:
                cphoto.current = False
                addcover = CoverPhotos(cover=coverphoto, user_id=user_info.id, current=True)
                db.session.add(addcover)
            else:
                addcover = CoverPhotos(cover=coverphoto, user_id=user_info.id, current=True)
                db.session.add(addcover)

        db.session.commit()
        flash('User details updated Successfully')
        return redirect(url_for('users.settings'))
    newform = NewPostForm()
    searchform = SearchForm()
    if searchform.validate_on_submit():
        search = searchform.search.data
        return redirect(url_for('users.search', search=search))
    return render_template("settings.html", user_info=user_info, form=form, details=details,
                           pagename=pagename, searchform=searchform, newform=newform, profilepic=profilepic,
                           followers=followers)



################################### route and function for user feed ########################################
@users_blueprint.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    details = WebSettings.query.all()
    pagename = 'Feed'
    user = current_user.username
    user_info = User.query.filter_by(username=user).first()
    profilepic = ProfilePhotos.query.filter_by(current=True ,user_id=user_info.id).first()
    follow_lst = FollowList.query.filter_by(user_id=user_info.id).all()
    friend_suggestions = User.query.filter(User.username != user).order_by(func.rand()).limit(11)

    followers = len(FollowList.query.filter_by(f_id=user_info.id).all())
    newform = NewPostForm()
    cform =CommentForm()
    if newform.validate_on_submit():
        name = user_info.firstname + ' ' + user_info.lastname
        if newform.files.data:
            fileis = newform.files.data
            fname = fileis.filename
            valu = fname.split('.')
            a = []
            b = []
            for i in IMAGES:
                a.append(i)
            for j in VIDEOS:
                b.append(j)
            if valu[1] in a:
                filename = images.save(newform.files.data)
                desc = newform.desc.data
                ptype = newform.ptype.data
                filetype = 'image'
                newpost = Posts(filename=filename, desc=desc, type=ptype, user_id=user_info.id, name=name,
                                filetype=filetype, profilephoto=profilepic.profile)
                db.session.add(newpost)
                db.session.commit()
                return redirect(url_for('users.profile'))

            elif valu[1] in b:
                filename = videos.save(newform.files.data)
                desc = newform.desc.data
                ptype = newform.ptype.data
                filetype = 'video'
                newpost = Posts(filename=filename, desc=desc, type=ptype, user_id=user_info.id, name=name,
                                filetype=filetype, profilephoto=profilepic.profile)
                db.session.add(newpost)
                db.session.commit()
                redirect(url_for('users.profile'))
        else:
            filename = 'Null'
            desc = newform.desc.data
            ptype = newform.ptype.data
            filetype = 'simple'
            newpost = Posts(filename=filename, desc=desc, type=ptype, user_id=user_info.id, name=name,
                            filetype=filetype, profilephoto=profilepic.profile)
            db.session.add(newpost)
            db.session.commit()
            redirect(url_for('users.profile'))

    searchform = SearchForm()
    if searchform.validate_on_submit():
        search = searchform.search.data
        return redirect(url_for('users.search', search=search))

    def get_profilepic(res):
        profile = ProfilePhotos.query.filter_by(current=True, user_id=res.id).first()
        if profile:
            return profile.profile

            ############### for checking if user followed ##############
    def is_follow(res, follow_lst):
         status = False
         for req in follow_lst:
            if res.id == req.f_id:
                status = True
         return status

    #############for showing posts###############
    friends = FriendsList.query.filter_by(user_id=user_info.id).all()
    viewposts = []
    videoposts = []

    for friend in friends:
        fposts = Posts.query.filter_by(user_id=friend.frnd_id).all()
        for v in fposts:
            if v.filetype == "video":
                videoposts.append(v)
        for p in fposts:
            viewposts.append(p)


    return render_template("feed.html", user_info=user_info, details=details, pagename=pagename,
                           searchform=searchform, newform=newform, profilepic=profilepic, followers=followers,
                            viewposts=reversed(viewposts), videos=reversed(videoposts), cform=cform,
                           fsuggestions=friend_suggestions, profil=get_profilepic, is_follow=is_follow,
                           follow_lst=follow_lst)


################################### route and function user search ########################################
@users_blueprint.route('/search/<string:search>', methods=['GET', 'POST'])
@login_required
def search(search):
    pagename = 'Search'
    user = current_user.username
    user_info = User.query.filter_by(username=user).first()
    profilepic = ProfilePhotos.query.filter_by(current=True, user_id=user_info.id).first()
    frnd_lst = FriendsList.query.filter_by(user_id=user_info.id).all()
    follow_lst = FollowList.query.filter_by(user_id=user_info.id).all()
    followers = len(FollowList.query.filter_by(f_id=user_info.id).all())
    req_lst = FriendsReq.query.filter_by(user_id=user_info.id).all()
    pen_lst = FriendsPen.query.filter_by(user_id=user_info.id).all()

    newform = NewPostForm()
    details = WebSettings.query.all()
    results = search.split(' ')
    result = set()
    for i in results:
            res2 = User.query.filter_by(firstname=i).all()
            res3 = User.query.filter_by(lastname=i).all()
            res1 = User.query.filter_by(username=i).all()
            if res1 and res2 and res3:
                for i in res1:
                    if i.is_active():
                        result.add(i)
            elif res1 and res2:
                for i in res1:
                    if i.is_active():
                        result.add(i)

            elif res1 and res3:
                for i in res1:
                    if i.is_active():
                        result.add(i)
                for i in res3:
                    if i.is_active():
                        result.add(i)
            elif res2 and res3:
                for i in res2:
                    if i.is_active():
                        result.add(i)
                for i in res3:
                    if i.is_active():
                        result.add(i)
            elif res1:
                for i in res1:
                    if i.is_active():
                        result.add(i)
            elif res2:
                for i in res2:
                    if i.is_active():
                        result.add(i)
            elif res3:
                for i in res3:
                    if i.is_active():
                        result.add(i)

    if len(result)>0:
        def get_profilepic(res):
            profile = ProfilePhotos.query.filter_by(current=True, user_id=res.id).first()
            if profile:
                return profile.profile

################# for checking if request is sent##############
        def is_req(res, pen_lst):
            status = False
            for req in pen_lst:
                if req.pen_id == res.id:
                    status = True
            return status

############### for checking if request is received ##############

        def is_pen(res, req_lst):
            status = False
            for req in req_lst:
                if req.req_id == res.id:
                    status = True
            return status

############### for checking if user followed ##############
        def is_follow(res, follow_lst):
            status = False
            for req in follow_lst:
                if res.id == req.f_id:
                    status = True
            return status

############### for checking if user is friend ##############
        def is_frnd(res, frnd_lst):
            status = False
            for req in frnd_lst:
                if res.id == req.frnd_id:
                    status = True
            return status

        searchform = SearchForm()
        if searchform.validate_on_submit():
            search = searchform.search.data
            return redirect(url_for('users.search', search=search))
        return render_template('searchresult.html', result=result, details=details, searchform=searchform,
                               user_info=user_info, pagename=pagename, pen_lst=pen_lst, req_lst=req_lst,
                               frnd_lst=frnd_lst, search=search, profil=get_profilepic,
                               newform=newform, profilepic=profilepic, followers=followers, follow_lst=follow_lst,
                               is_frnd=is_frnd, is_pen=is_pen, is_follow=is_follow, is_req=is_req)
    else:
        searchform = SearchForm()
        if searchform.validate_on_submit():
            search = searchform.search.data
            return redirect(url_for('users.search', search=search))
        flash('User not found')
        return render_template('searchresult.html', details=details, searchform=searchform,
                               user_info=user_info, pagename=pagename, search=search, profilepic=profilepic,
                               followers=followers)


################################### function for adding friend ########################################
@users_blueprint.route('/addfriend/<string:id>', methods=['GET', 'POST'])
@login_required
def addfriend(id):
    users = current_user.username
    user = db.session.query(User.id).filter(User.username == users).first()
    uid = user.id
    rid = id
    addreq = FriendsReq(user_id=rid, req_id=uid)
    addpen = FriendsPen(user_id=uid, pen_id=rid)
    db.session.add(addreq)
    db.session.add(addpen)
    db.session.commit()
    flash('Friend Request Sent')
    return redirect(request.referrer)

################################### function for accepting friend request ########################################
@users_blueprint.route('/acceptreq/<string:rid>/<string:uid>', methods=['GET', 'POST'])
@login_required
def acceptreq(rid, uid):
    req_lst = FriendsReq.query.filter_by(user_id=uid, req_id=rid).first()
    pen_lst = FriendsPen.query.filter_by(user_id=rid, pen_id=uid).first()
    frnd1 = FriendsList(frnd_id=rid, user_id=uid)
    frnd2 = FriendsList(frnd_id=uid, user_id=rid)
    db.session.add(frnd1)
    db.session.add(frnd2)
    db.session.delete(req_lst)
    db.session.delete(pen_lst)
    db.session.commit()
    flash('Friend Added')
    return redirect(request.referrer)


################################### function for canceling/deleting friend request ########################################
@users_blueprint.route('/cancelreq/<string:rid>/<string:uid>', methods=['GET', 'POST'])
@login_required
def cancelreq(rid, uid):
    req_lst = FriendsReq.query.filter_by(user_id=uid, req_id=rid).first()
    pen_lst = FriendsPen.query.filter_by(user_id=rid, pen_id=uid).first()
    db.session.delete(req_lst)
    db.session.delete(pen_lst)
    db.session.commit()
    flash('Friend Request Canceled')
    return redirect(request.referrer)

################################### function for unfriend user ########################################
@users_blueprint.route('/unfriend/<string:rid>/<string:uid>', methods=['GET', 'POST'])
@login_required
def unfriend(rid, uid):
    frnd1 = FriendsList.query.filter_by(user_id=rid).first()
    frnd2 = FriendsList.query.filter_by(user_id=uid).first()
    db.session.delete(frnd1)
    db.session.delete(frnd2)
    db.session.commit()
    flash('Friend Removed')
    return redirect(request.referrer)

################################### function for following user ########################################
@users_blueprint.route('/follow/<string:rid>/<string:uid>', methods=['GET', 'POST'])
@login_required
def follow(rid, uid):
    follow1 = FollowList(f_id=rid, user_id=uid)
    db.session.add(follow1)
    db.session.commit()
    flash('User Followed')
    return redirect(request.referrer)

################################### function for unfollowing user ########################################
@users_blueprint.route('/unfollow/<string:rid>/<string:uid>', methods=['GET', 'POST'])
@login_required
def unfollow(rid, uid):
    follow1 = FollowList.query.filter_by(f_id=rid, user_id=uid).first()
    db.session.delete(follow1)
    db.session.commit()
    flash('User Unfollowed')
    return redirect(request.referrer)

################################### function to like post ########################################
@users_blueprint.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Posts.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)


################################### function to comment on post ########################################
@users_blueprint.route('/comments/<int:post_id>/<action>', methods=['GET', 'POST'])
@login_required
def comments(post_id, action):
    post = Posts.query.filter_by(id=post_id).first_or_404()
    profilepic = ProfilePhotos.query.filter_by(current=True, user_id=current_user.id).first()
    cform = CommentForm()
    if cform.validate_on_submit():
        if action == 'comment':
            name = current_user.firstname + ' ' + current_user.lastname

            comment = PostComment(comment=cform.comment.data, name=name, photo=profilepic.profile, user_id=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            return redirect(request.referrer)

################################### route and function user profile(other) ########################################
@users_blueprint.route('/userprofile/<string:username>', methods=['GET', 'POST'])
@login_required
def userprofile(username):
    pagename = 'User Profile'
    details = WebSettings.query.all()
    viewuser = User.query.filter_by(username=username).first()
    user_info = User.query.filter_by(id=current_user.id).first()
    userpic = ProfilePhotos.query.filter_by(current=True, user_id=viewuser.id).first()
    profilepic = ProfilePhotos.query.filter_by(current=True, user_id=user_info.id).first()
    coverpic = CoverPhotos.query.filter_by(current=True, user_id=viewuser.id).first()
    friends = FriendsList.query.filter_by(user_id=viewuser.id).all()
    following = FollowList.query.filter_by(user_id=viewuser.id).all()
    followers = FollowList.query.filter_by(f_id=viewuser.id).all()
    follow_lst = FollowList.query.filter_by(user_id=user_info.id).all()
    posts = Posts.query.filter_by(user_id=viewuser.id).all()
    newform = NewPostForm()

    cform = CommentForm()

    def get_profilepic(res):
        profile = ProfilePhotos.query.filter_by(current=True, user_id=res.id).first()
        if profile:
            return profile.profile

            ############### for checking if user followed ##############
    def is_follow(res, follow_lst):
         status = False
         for req in follow_lst:
            if res.id == req.f_id:
                status = True
         return status

    ############# for showing posts ###########

    viewposts = []
    videoposts = []
    for p in posts:
        viewposts.append(p)
    for v in posts:
        if v.filetype == "video":
            videoposts.append(v)

    searchform = SearchForm()
    if searchform.validate_on_submit():
        search = searchform.search.data
        return redirect(url_for('users.search', search=search))
    return render_template("userprofile.html", newform=newform, user_info=user_info, details=details,
                           pagename=pagename, searchform=searchform, profilepic=profilepic, coverpic=coverpic,
                           friends=len(friends), followers=len(followers), following=len(following), posts=len(posts),
                           allposts=reversed(viewposts), videos=reversed(videoposts), viewuser=viewuser, cform=cform,
                           userpic=userpic, follow_lst=follow_lst, get_profilepic=get_profilepic, is_follow=is_follow)

################################### route and function for help(for future implementation) ########################################
@users_blueprint.route('/help')
@login_required
def help():
    return render_template('help.html')


################################### route and function to show live stream ########################################
@users_blueprint.route('/live', methods=['GET', 'POST'])
@login_required
def live():
    pagename = 'Live'
    details = WebSettings.query.all()
    user_info = User.query.filter_by(id=current_user.id).first()
    followers = len(FollowList.query.filter_by(f_id=user_info.id).all())
    newform = NewPostForm()
    searchform = SearchForm()
    if searchform.validate_on_submit():
        search = searchform.search.data
        return redirect(url_for('users.search', search=search))
    return render_template('live.html', newform=newform, details=details, searchform=searchform, user_info=user_info,
                           pagename=pagename, followers=followers)





