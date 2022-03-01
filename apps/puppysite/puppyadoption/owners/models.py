from puppyadoption import db

class Owner(db.Model) :

    __tablename__ = "owner"

    id = db.Column(db.Integer,primary_key=True)
    Owner_name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer,db.ForeignKey('pup.id'))
    def __init__(self,own_name,puppy_id):
        self.Owner_name = own_name
        self.puppy_id = puppy_id
