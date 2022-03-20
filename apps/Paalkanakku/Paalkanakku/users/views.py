try:
    from Paalkanakku import app, db
    from Paalkanakku.models import User, GoogleData
    from Paalkanakku.users.forms import RegistrationForm, UpdateUserForm, LoginForm
    from Paalkanakku.users.picture_handler import add_profile_pic
    #from Paalkanakku.config import google
except:
    from Paalkanakku.Paalkanakku import app, db
    from Paalkanakku.Paalkanakku.models import User,GoogleData
    from Paalkanakku.Paalkanakku.users.forms import RegistrationForm, UpdateUserForm, LoginForm
    from Paalkanakku.Paalkanakku.users.picture_handler import add_profile_pic
    #from Paalkanakku.Paalkanakku.config import google

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

users = Blueprint('users', __name__)


@users.route('/reg', methods=['POST','GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data
                    )
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash("Your email is already registered.Try Log in")
        else:
            flash("You are Successfully Registered!")
            return redirect(url_for('users.login'))

    return render_template('register.html', form=form, flash=form.errors)


@users.route('/login', methods=['POST','GET'])
def login():

    form = LoginForm()
    error = []

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        try:
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
            else:
                flash("Email or password is wrong")
                return render_template('login.html', form=form)
        except:
            error.append('Oho!')
            flash("Email is not Registered.")
            return render_template('login.html', form=form)
        else:
            flash("You are logged in!")
            print ("Logged in ", request.args.get('next'))
            next_page = request.args.get('next')
            if next_page is None or not next_page[0] == '/':
                next_page = url_for('core.index')
            return redirect(next_page)

    return render_template('login.html',form=form,flash=form.errors,error=error)


@users.route('/logout')
def logout():
    logout_user()
    flash("You are logged out!")
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    #print (form.data,"after")

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            #print ("Inside valida form", pic)
            current_user.profile_image = pic

        try:
            current_user.username = form.username.data
            db.session.commit()
        except:
            flash(f"Username taken already")
        else:
            try:
                current_user.email = form.email.data
                db.session.commit()
            except:
                flash(f"Email registered already")
            else:
                db.session.commit()
                flash("Your Profile Updated!")

        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        #print ("form invalid")
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    #print (profile_image,"profile_pic name")
    return render_template('account.html',profile_image=profile_image,form=form,flash=form.errors)






"""
@users.route('/log')
def index():
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    #print(resp.json())
    email = resp.json()['email']
    return render_template('index.html', email=email)


@users.route('/login/google')
def login():
    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get("/plus/v1/people/me")
    assert resp.ok, resp.text
    #print(resp.json())
    email = resp.json()['email']
    return render_template('index.html', email=email)
"""