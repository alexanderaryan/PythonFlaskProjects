try:
    from Paalkanakku import db, login_manager
except:
    from Paalkanakku.Paalkanakku import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    google = db.relationship('GoogleData', backref='username', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        print (generate_password_hash(password),"came the password")
        self.password_hash = generate_password_hash(password)
        print("created user")

    def check_password(self, password):
        print ("Iam here within check pw")
        print (password,'rec pw')
        print(self.email, 'stored email')
        print (self.username,'stored uname')
        print(self.password_hash, 'pw_hash')
        print(self.username, 'user')
        print (check_password_hash(self.password_hash, password),"Pw authenticated successfully")
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"


class GoogleData(db.Model):

    __tablename__ = 'Google_data'

    users = db.relationship(User)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sheet_name = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    sheet_link = db.Column(db.Text, unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, user_id, sheet_name, sheet_link):
        self.user_id = user_id
        self.sheet_name = sheet_name
        self.sheet_link = sheet_link

    def __repr__(self):
        return f"Google Sheet Name : {self.sheet_name}"