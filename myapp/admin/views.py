import os
from flask import Blueprint, render_template, redirect, flash, url_for, request, session
from myapp import db, images, app
from flask_login import login_user, login_required, logout_user
from myapp.models import User, WebSettings, Posts
from myapp.admin.forms import AdminSignUp, AdminSignIn, WebSetting


admin_blueprint = Blueprint('admin', __name__, template_folder='templates/admin')

@admin_blueprint.route('/', methods=['GET', 'POST'])
def loginsignup():
    snumb = "1234567890"

    special_character = "1234567890"

    def is_valid(username):
        global special_character
        return any(char in snumb for char in username)

    sform = AdminSignUp()
    form = AdminSignIn()
    details = WebSettings.query.all()
    detail = WebSettings.query.first()

    if sform.validate_on_submit():
        if detail is None:

            name = "Unity Streak"
            favicon = "favicon.png"
            logo = "logo.png"
            copyrights = "Unity Streak 2021"
            lsliderone = "Welcome to Unity Streak"
            lonedesc = "Some description here"
            lonephoto = "lphoto.png"
            lslidertwo = "Welcome to Unity Streak"
            ltwodesc = "Some description here"
            ltwophoto = "lphoto.png"
            lsliderthree = "Welcome to Unity Streak"
            lthreedesc = "Some description here"
            lthreephoto = "lphoto.png"
            swenheading = "Welcome to Unity Streak"
            sdesc = "Social Media Application"
            lphoto = "lphoto.png"
            signup = True

            adddata = WebSettings(name=name, favicon=favicon, logo=logo, copyrights=copyrights, lsliderone=lsliderone,
                                  lonedesc=lonedesc, lonephoto=lonephoto, lslidertwo=lslidertwo, ltwodesc=ltwodesc,
                                  ltwophoto=ltwophoto, lsliderthree=lsliderthree, lthreedesc=lthreedesc,
                                  lthreephoto=lthreephoto, swebheading=swenheading, sdesc=sdesc, lphoto=lphoto,
                                  signup=signup)
            db.session.add(adddata)
            db.session.commit()


            email = User.query.filter_by(email=sform.email.data).first()
            if email is None:
                username = User.query.filter_by(username=sform.user.data).first()
                if username is None:
                    if is_valid( sform.user.data):
                        desc = 'Your Description Here'
                        facebook = 'Facebook Profile'
                        instagram = 'Instagram Profile'
                        admin = User(firstname=None, lastname=None, email=sform.email.data, dob=None, username=sform.user.data,
                                     gender=None, authenticated=True, password=sform.password.data, role=True, desc=desc,
                                     facebook=facebook, instagram=instagram)
                        db.session.add(admin)
                        db.session.commit()
                        flash('Account Created Successfully')
                        return redirect(url_for('admin.loginsignup'))
                    else:
                        flash('Username must contain at least one number')
                        return redirect(url_for('users.signup'))
                else:
                    flash('Username already exists, please try again!')
                    return redirect(url_for('admin.loginsignup'))
            else:
                flash('Email already exists, please try logging in!')
                return redirect(url_for('admin.loginsignup'))

        elif detail.signup == True:
            if sform.validate_on_submit():
                email = User.query.filter_by(email=sform.email.data).first()
                if email is None:
                    username = User.query.filter_by(username=sform.user.data).first()
                    if username is None:
                        if is_valid( sform.user.data):
                            desc = 'Your Description Here'
                            facebook = 'Facebook Profile'
                            instagram = 'Instagram Profile'
                            admin = User(firstname=None, lastname=None, email=sform.email.data, dob=None, username=sform.user.data,
                                         gender=None, authenticated=True, password=sform.password.data, role=True, desc=desc,
                                         facebook=facebook, instagram=instagram)
                            db.session.add(admin)
                            db.session.commit()
                            flash('Account Created Successfully')
                            return redirect(url_for('admin.loginsignup'))
                        else:
                            flash('Username must contain at least one number')
                            return redirect(url_for('users.signup'))
                    else:
                        flash('Username already exists, please try again!')
                        return redirect(url_for('admin.loginsignup'))
                else:
                    flash('Email already exists, please try logging in!')
                    return redirect(url_for('admin.loginsignup'))
        else:
            flash('Unauthorised attempt! Please signup here!')
            return redirect(url_for('users.signup'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                session['user'] = form.user.data
                status = user.is_active() and user.is_admin()
                if status:
                    login_user(user)
                    next = request.args.get('next')
                    if next == None or not next[0] == '/':
                        next = url_for('admin.dashboard')
                        return redirect(next)
                else:
                    flash('You are not authorised to login! Login Here')
                    return redirect(url_for('users.signin'))

            else:
                flash('Wrong Password')
                return redirect(url_for('admin.loginsignup'))

        else:
            flash('Username not found')
            return redirect(url_for('admin.loginsignup'))
    return render_template('loginregister.html', sform=sform, form=form, details=details)


@admin_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.loginsignup'))


@admin_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = session['user']
    user_info = User.query.filter_by(username=user).first()
    status = user_info.is_admin()
    if status:
        pagename = 'Dashboard'
        details = WebSettings.query.all()
        posts = Posts.query.all()
        page = request.args.get('page', 1, type=int)
        new_users = User.query.filter_by(authenticated=False).paginate(page, app.config['USERS_PER_TABLE'], False)
        nnext_url = url_for('admin.dashboard', page=new_users.next_num) \
            if new_users.has_next else None
        nprev_url = url_for('admin.dashboard', page=new_users.prev_num) \
            if new_users.has_prev else None

        active_users = User.query.filter(User.id!=user_info.id).paginate(page, app.config['USERS_PER_TABLE'], False)

        total = User.query.all()
        total_users = len(total)


        next_url = url_for('admin.dashboard', page=active_users.next_num) \
            if active_users.has_next else None
        prev_url = url_for('admin.dashboard', page=active_users.prev_num) \
            if active_users.has_prev else None

        return render_template('dashboard.html', user=user, new_users=new_users, active_users=active_users,
                                   total_users=total_users, details=details, pagename=pagename, next_url=next_url,
                           prev_url=prev_url, nnext_url=nnext_url, nprev_url=nprev_url, active=len(active_users.items),
                               posts=len(posts))

    else:
        logout_user()
        return redirect(url_for('users.signin'))


@admin_blueprint.route('/newusers', methods=['GET', 'POST'])
@login_required
def newusers():
    user = session['user']
    user_info = User.query.filter_by(username=user).first()
    status = user_info.is_admin()
    if status:
        pagename = 'New Users'
        details = WebSettings.query.all()
        page = request.args.get('page', 1, type=int)
        new_users = User.query.filter_by(authenticated=False).paginate(page, app.config['USERS_PER_TABLE'], False)
        next_url = url_for('admin.newusers', page=new_users.next_num) \
            if new_users.has_next else None
        prev_url = url_for('admin.newusers', page=new_users.prev_num) \
            if new_users.has_prev else None

        return render_template('newusers.html', user=user, new_users=new_users, details=details, pagename=pagename,
                               next_url=next_url, prev_url=prev_url)


    else:
        logout_user()
        return redirect(url_for('users.signin'))

@admin_blueprint.route('/activate/<string:id>', methods=['GET', 'POST'])
@login_required
def activate(id):
    user = session['user']
    user_info = User.query.filter_by(username=user).first()
    status = user_info.is_admin()
    if status:
        user = User.query.filter_by(id=id).first()
        user.authenticated = True
        db.session.commit()
        flash('User Activated')
        return redirect(request.referrer)
    else:
        logout_user()
        return redirect(url_for('users.signin'))

@admin_blueprint.route('/deactivate/<string:id>', methods=['GET', 'POST'])
@login_required
def deactivate(id):
    user = session['user']
    user_info = User.query.filter_by(username=user).first()
    status = user_info.is_admin()
    if status:
        user = User.query.filter_by(id=id).first()
        user.authenticated = False
        db.session.commit()
        flash('User Deactivated')
        return redirect(request.referrer)
    else:
        logout_user()
        return redirect(url_for('users.signin'))

@admin_blueprint.route('/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user = session['user']
    user_info = User.query.filter_by(username=user).first()
    status = user_info.is_admin()
    if status:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash('User Deleted')
        return redirect(request.referrer)
    else:
        logout_user()
        return redirect(url_for('users.signin'))



# @admin_blueprint.route('/analytics', methods=['GET', 'POST'])
# @login_required
# def analytics():
#     user = session['user']
#     user_info = User.query.filter_by(username=user).first()
#     status = user_info.is_admin()
#
#     if status:
#         details = WebSettings.query.all()
#         return render_template('analytics.html', user=user, details=details)
#     else:
#         logout_user()
#         return redirect(url_for('users.signin'))


@admin_blueprint.route('/websettings', methods=['GET', 'POST'])
@login_required
def websettings():
    user = session['user']
    user_info = User.query.filter_by(username=user).first()
    status = user_info.is_admin()
    if status:
        detail = WebSettings.query.first()
        details = [detail]
        pagename = 'Website Settings'
        if details:
            form = WebSetting(obj=detail)
            if form.validate_on_submit():
                detailss = WebSettings.query.first()
                # form.populate_obj(detailss)
                detailss.name = form.name.data
                detailss.copyrights = form.copyrights.data
                detailss.lsliderone = form.lsliderone.data
                detailss.lonedesc = form.lonedesc.data
                detailss.lslidertwo = form.lslidertwo.data
                detailss.ltwodesc = form.ltwodesc.data
                detailss.lsliderthree = form.lsliderthree.data
                detailss.lthreedesc = form.lthreedesc.data
                detailss.swenheading = form.swebheading.data
                detailss.sdesc = form.sdesc.data
                detailss.signup = form.signup.data
                if form.favicon.data:
                    filename = images.path(detailss.favicon)
                    os.remove(filename)
                    detailss.favicon = images.save(form.favicon.data)
                if form.logo.data:
                    filename = images.path(detailss.logo)
                    os.remove(filename)
                    detailss.logo = images.save(form.logo.data)
                if form.lonephoto.data:
                    filename = images.path(detailss.lonephoto)
                    os.remove(filename)
                    detailss.lonephoto = images.save(form.lonephoto.data)
                if form.ltwophoto.data:
                    filename = images.path(detailss.ltwophoto)
                    os.remove(filename)
                    detailss.ltwophoto = images.save(form.ltwophoto.data)
                if form.lthreephoto.data:
                    filename = images.path(detailss.lthreephoto)
                    os.remove(filename)
                    detailss.lthreephoto = images.save(form.lthreephoto.data)
                if form.lphoto.data:
                    filename = images.path(detailss.lphoto)
                    os.remove(filename)
                    detailss.lphoto = images.save(form.lphoto.data)
                # if form.signup.name == "On":
                #     signup = True
                #     detailss.signup = signup
                # elif form.signup.name == "Off":
                #     signup = False
                #     detailss.signup = signup

                db.session.commit()
                flash("Details Updated Successfully")
                return render_template('websetting.html', user=user, form=form, details=details, pagename=pagename,)
            return render_template('websetting.html', user=user, form=form, details=details, pagename=pagename)
        else:
            form = WebSetting()
            if form.validate_on_submit():
                name = form.name.data
                favicon = images.save(form.favicon.data)
                logo = images.save(form.logo.data)
                copyrights = form.copyrights.data
                lsliderone = form.lsliderone.data
                lonedesc = form.lonedesc.data
                lonephoto = images.save(form.lonephoto.data)
                lslidertwo = form.lslidertwo.data
                ltwodesc = form.ltwodesc.data
                ltwophoto = images.save(form.ltwophoto.data)
                lsliderthree = form.lsliderthree.data
                lthreedesc = form.lthreedesc.data
                lthreephoto = images.save(form.lthreephoto.data)
                swenheading = form.swebheading.data
                sdesc = form.sdesc.data
                lphoto = images.save(form.lphoto.data)
                if form.signup.data == "On":
                    signup = True
                else:
                    signup = False
                adddata = WebSettings(name=name, favicon=favicon, logo=logo, copyrights=copyrights, lsliderone=lsliderone,
                                  lonedesc=lonedesc, lonephoto=lonephoto, lslidertwo=lslidertwo, ltwodesc=ltwodesc,
                                  ltwophoto=ltwophoto, lsliderthree=lsliderthree, lthreedesc=lthreedesc,
                                  lthreephoto=lthreephoto, swebheading=swenheading, sdesc=sdesc, lphoto=lphoto, signup=signup)
                db.session.add(adddata)
                db.session.commit()
                flash('Details Saved Successfully')
                return redirect(url_for('admin.websettings'))
            return render_template('websettings.html', user=user, form=form, pagename=pagename)
    else:
        logout_user()
        return redirect(url_for('users.signin'))







