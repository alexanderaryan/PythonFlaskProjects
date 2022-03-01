from puppyadoption import app, db, render_template, redirect, url_for, flash,\
    abort, login_required,logout_user,login_user,puppies_blueprint,owners_blueprint,request

from puppyadoption.users.models import User
from puppyadoption.users.forms import Login,RegistrationForm

@app.route('/')
def index():
    return render_template("home.html")



@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('/home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out")
    return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():

    form = Login()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.checkpassword(form.password.data) and user is not None:
            login_user(user)
            flash("You have logged in Succesfully")

            next = request.args.get('next')

            if next is None or not next[0] == '/':
                next = url_for('index')

            return redirect(next)


    return render_template('/login.html',form=form)


@app.route('/register',methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your are Registered Successfully")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


if __name__ == "__main__":
    app.run(debug=True)