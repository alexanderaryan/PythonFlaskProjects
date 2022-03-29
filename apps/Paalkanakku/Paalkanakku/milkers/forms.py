from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
    BooleanField, SelectMultipleField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

try:
    from Paalkanakku.models import Milk
except:
    from Paalkanakku.Paalkanakku.models import Milk


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
    submit = SubmitField('Delete')
