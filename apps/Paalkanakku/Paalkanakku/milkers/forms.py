from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
    BooleanField, SelectMultipleField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms import ValidationError

try:
    from Paalkanakku.models import Milk, Milkers
except:
    from Paalkanakku.Paalkanakku.models import Milk, Milkers


def milker_data(active=True):
    try:
        if active:
            milkers_data = Milkers.query.all()
        else:
            milkers_data = Milkers.query.filter(Milkers.active==True).all()
    except:
        print ("Milker table is empty")
        milkers_data = None
        milker_ids = []
        milkers = [(1, 'Add Milker Data') ]
    else:
        milker_ids = [milker.milker_id for milker in milkers_data]
        milkers = [(milker.milker_id, milker.name) for milker in milkers_data]
    return milkers_data, milker_ids, milkers


class AddMilkForm(FlaskForm):

    #owner_id=IntegerField('CustomerId', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(),Length(max=30,message="Max 30 characters")])
    place = StringField('Place', validators=[DataRequired(),Length(max=30,message="Max 30 characters")])
    #Milker = StringField('MilkerId', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired(),
                                              NumberRange(min=0, max=30000,message='Salary should be less than 30k')])
    bike = StringField('Bike', validators=[DataRequired(),Length(min=0,max=15,message="Bike 15 characters")])
    #owner_id = SelectField('CustomerId', choices='', validators=[])
    submit = SubmitField('Add')


class DeleteMilkForm(FlaskForm):

    checkbox = BooleanField("Delete")
    #checkbox = SelectField(u'Delete',choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Update')
