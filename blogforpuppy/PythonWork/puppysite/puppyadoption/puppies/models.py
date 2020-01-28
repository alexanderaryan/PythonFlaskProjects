from puppyadoption import db

class Puppy(db.Model):

    __tablename__ = "pup"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    owner = db.relationship('Owner',backref='Puppy',uselist=False)
    def __init__(self,name):
        self.name = name
        print (self.name)
    def __repr__(self):
        if self.owner:
            return f"Puppy Name: {self.name} and its id {self.id} and it's owner is {self.owner.Owner_name}"
        else:
            return f"Puppy Name: {self.name} and its id {self.id} and it has no owner yet"
