from puppyblog import render_template,url_for,flash,request,\
    redirect,Blueprint,login_user,logout_user,login_required,current_user,db

from puppyblog.users.models import Users
from puppyblog.blog_posts.models import Blogpost
from puppyblog.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from puppyblog.users.picture_handler import add_profile_pic

users_blueprint = Blueprint('users_blueprint',__name__)


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users_blueprint.route('/register',methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = Users(email=form.email.data,
                     username=form.username.data,
                     password=form.password.data,
                     sex=form.sex.data,
                     mobile=str(form.country_code.data)+str(form.mobile.data))
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash("Your email is already registered.Try Log in")
        else:
            flash("Thanks for Registration!")

        return redirect(url_for('users_blueprint.login'))
    print (form.errors)
    return render_template('register.html', form=form,flash=form.errors)


@users_blueprint.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    error = []

    if form.validate_on_submit():

        user = Users.query.filter_by(email=form.email.data).first()



        try:
            if user.check_password(form.password.data) and user is not None:
                login_user(user)
        except:
            error.append('Oho!')
            flash ("Email is not Registered.")
            return render_template('login.html', form=form)
        else:
                next= request.args.get('next')

                if next is None or not next[0] == '/':
                    next = url_for('core.index')

                return redirect(next)

    return render_template('login.html',form=form,flash=form.errors,error=error)


@users_blueprint.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)

            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash("Your Account Data updated!")

        return redirect(url_for('users_blueprint.account',flash=flash))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='/profile_pics'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)

@users_blueprint.route('/<username>')
@login_required
def userposts(username):
    page = request.args.get('page',1,type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    blog_posts = Blogpost.query.filter_by(author=user).order_by(Blogpost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)







