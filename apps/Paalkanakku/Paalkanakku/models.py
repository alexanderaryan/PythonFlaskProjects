from sqlalchemy import UniqueConstraint
#from sqlalchemy.orm import validates
try:
    from Paalkanakku import db, login_manager
except:
    from Paalkanakku.Paalkanakku import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


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


class Milkers(db.Model,UserMixin):

    __tablename__ = 'milkers'

    milker_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False,index=True)
    place = db.Column(db.String(64), nullable=False,index=True)
    bike = db.Column(db.String(64), nullable=True)
    salary = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, unique=False, default=True)
    #owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'), nullable=True)
    owner = db.relationship('CowOwner', backref='milker', lazy='dynamic')

    #milk = db.relationship('Milk', backref='owner', lazy=True)

    def __init__(self, name, place, bike, salary):
        self.name = name
        self.place = place
        self.bike = bike
        self.salary = salary


    def __repr__(self):
        return f"Milker {self.name} {self.milker_id} from {self.place} is {self.active}"

    def milker_customers(self):
        return self.owner.all()


class CowOwner(db.Model, UserMixin):

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64), index=True)
    place = db.Column(db.String(64), index=True)
    cows = db.Column(db.Integer)
    milker_id = db.Column(db.Integer, db.ForeignKey('milkers.milker_id'), nullable=False)
    active = db.Column(db.Boolean, unique=False, default=True)

    #Adding after 2.0
    surname = db.Column(db.String(64),index=True)
    phone_number = db.Column(db.Integer)
    address_line2 = db.Column(db.String(64),index=True)
    pincode = db.Column(db.Integer)
    email = db.Column(db.String(64), index=True)
    dairy_loan = db.Column(db.Integer)
    kcc_loan = db.Column(db.Integer)
    country = db.Column(db.String(64))
    state = db.Column(db.String(64))
    profile_pic_name = db.Column(db.String(64),default='default_profile.png')

    #own_cows = db.relationship('Cows', backref='owner', lazy='dynamic')
    milk = db.relationship('Milk', backref='owner', lazy=True)
    # milker = db.relationship('Milkers', backref='owner', lazy='dynamic')

    def __init__(self, owner_id, name, place, num_cows, milker_id,\
                 surname=None, phone=None, ad_2=None, pincode=None,
                 email=None, dairy_loan=0, kcc_loan=0,
                 country="இந்தியா",state="தமிழ் நாடு"):
        self.owner_id = owner_id
        self.name = name
        self.place = place
        self.cows = num_cows
        self.milker_id = milker_id
        #After upgrade 2.0
        self.email = email
        self.surname = surname
        self.address_line2 = ad_2
        self.phone_number = phone
        self.pincode = pincode
        self.dairy_loan = dairy_loan
        self.kcc_loan = kcc_loan
        self.country = country
        self.state = state

    def __repr__(self):
        return f"Owner {self.name} place {self.place} num_cows {self.cows} milker {self.milker_id}"

    def cows_and_owners(self):
        return self.milk.all()

    def milker_list(self):
        return self.milker_id


class Milk(db.Model,UserMixin):

    __tablename__ = "milk"

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True,index=True)
    #id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer,db.ForeignKey('owners.owner_id'),nullable=False)
    milker_id = db.Column(db.Integer, db.ForeignKey('milkers.milker_id'), nullable=False, index=True)
    milked_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    am_litre = db.Column(db.Float, nullable=True, default=0)
    pm_litre = db.Column(db.Float, nullable=True, default=0)
    price =  db.Column(db.Float, nullable=False)
    fodder = db.Column(db.Integer)
    advance = db.Column(db.Integer)
    loan = db.Column(db.Integer)
    dr_service = db.Column(db.Integer)

    __table_args__ = (UniqueConstraint('event_id','owner_id', 'milker_id','milked_date', name='_daily_milk_data'),
                     )

    def __init__(self,owner_id,milker,milked_date,milked_time,litre,ml,price,
                 fodder=0,
                 advance=0,
                 loan=0,
                 dr_service=0):

        self.owner_id=owner_id
        #self.name=name
        #self.place=place
        self.milker_id=milker
        self.milked_date=milked_date
        self.price = price
        self.loan = loan
        self.fodder = fodder
        self.advance = advance
        self.dr_service = dr_service
        if milked_time == "am":
            self.am_litre = self.litre_conv(litre,ml)
        else:
            self.pm_litre = self.litre_conv(litre,ml)

    def __repr__(self):
        return f"Date: {self.milked_date}"

    def litre_conv(self, l, ml):
        """To merge the litre and milli litre to single column value"""
        return float(str(l) + '.' + str(ml))

    def owner_details(self):
        return CowOwner.query.filter(CowOwner.owner_id == self.owner_id).first()


"""class Ledger(db.Model,UserMixin):

    __tablename__ = "ledger"

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True,index=True)
    #id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer,db.ForeignKey('owners.owner_id'),nullable=False)
    milker_id = db.Column(db.Integer, db.ForeignKey('milkers.milker_id'), nullable=False, index=True)
    milked_month = db.Column(db.String(10), nullable=False)
    milked_year = db.Column(db.Integer, nullable=False)
    milked_time = db.Column(db.String(4),nullable=False)
    litre = db.Column(db.Float, nullable=False)

    __table_args__ = (UniqueConstraint('event_id','owner_id', 'milker_id','milked_year','milked_month', name='_daily_milk_data'),
                     )

    def __init__(self,owner_id,milker,milked_month,milked_year,milked_time,litre):

        self.owner_id=owner_id
        self.milker_id=milker
        self.milked_month=milked_month
        self.milked_year=milked_year
        self.milked_time=milked_time
        self.litre=litre

    def __repr__(self):
        return f"Litre: {self.litre}"

    def ledger_details(self):
        return CowOwner.query.filter(CowOwner.owner_id == self.owner_id).first()
"""


class Cows(db.Model):

    __tablename__ = 'cows'

    cow_id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.owner_id'), nullable=False)
    average = db.Column(db.Float, nullable=True)
    milker_id = db.Column(db.Integer, db.ForeignKey('milkers.milker_id'), nullable=False)
    cows = db.relationship('Milkers', backref='milkers', lazy=True)

    def __init__(self, breed, owner_id, milker_id):
        self.breed = breed
        self.owner_id = owner_id
        self.milker_id = milker_id

    def __repr__(self):
        return f"{self.owners.name} is the owner of Cows : {self.cows}"

