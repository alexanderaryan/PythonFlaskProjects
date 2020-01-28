from puppyblog import db,generate_password_hash,check_password_hash,login_manager, datetime
from puppyblog.users.models import Users


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Blogpost(db.Model):

    __tablename__ = 'blog'

    users = db.relationship(Users)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable= False, default=datetime.utcnow)

    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)



    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id



    def __repr__(self):
        return f"Post ID:  {self.id} --Date:  {self.date} --Title {self.title}"



