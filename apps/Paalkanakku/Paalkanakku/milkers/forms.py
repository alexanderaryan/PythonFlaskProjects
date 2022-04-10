from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
    BooleanField, SelectMultipleField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
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
    name = StringField('Name', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    #Milker = StringField('MilkerId', validators=[DataRequired()])
    salary = FloatField('Salary', validators=[DataRequired()])
    bike = StringField('Bike', validators=[DataRequired()])
    #owner_id = SelectField('CustomerId', choices='', validators=[])
    submit = SubmitField('Add')


class DeleteMilkForm(FlaskForm):

    checkbox = BooleanField("Delete")
    #checkbox = SelectField(u'Delete',choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Update')
