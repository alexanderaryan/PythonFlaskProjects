from puppyadoption import db,login_manager, check_password_hash, generate_password_hash, UserMixin


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),index=True,unique=True)
    username = db.Column(db.String(64),index=True,unique=True)
    password_hashed = db.Column(db.String())

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hashed = generate_password_hash(password)

    def checkpassword(self,password):
        return check_password_hash(self.password_hashed,password)


