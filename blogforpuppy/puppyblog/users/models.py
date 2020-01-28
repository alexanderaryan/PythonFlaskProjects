from puppyblog import db,generate_password_hash,check_password_hash,login_manager,UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(30),nullable=False,default='default-profile-picture-man.jpg')
    email = db.Column(db.String(68),unique=True,index=True)
    mobile = db.Column(db.Integer,unique=True,nullable=True)
    username = db.Column(db.String(34),unique=True,index=True)
    password_hash = db.Column(db.String(128),nullable=False)
    sex = db.Column(db.String(10),nullable=True,default='m')

    posts = db.relationship('Blogpost',backref='author',lazy=True)

    def __init__(self,email,username,password,sex,mobile):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.sex = sex
        self.mobile = mobile


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"



