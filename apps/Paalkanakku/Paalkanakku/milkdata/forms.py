from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
    BooleanField, SelectMultipleField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms import ValidationError

from flask_login import current_user
try:
    from Paalkanakku.models import CowOwner
except:
    from Paalkanakku.Paalkanakku.models import CowOwner


class AddDailyData(FlaskForm):

    owner_id=IntegerField('CustomerId', validators=[DataRequired()])
    name = StringField('Name')
    place = StringField('Place')
    milker = SelectField('Milker', validators=[DataRequired()])
    milked_date = DateField('Date',validators=[DataRequired()])
    milked_time = SelectField('AM/PM',choices=[('am','AM'),('pm','PM')])
    litre = IntegerField('Litre',
                         validators=[DataRequired(),NumberRange(min=0, max=99, message='Max 3 digits')],
                         default=0)
    ml = IntegerField('MilliLitre',
                      validators=[DataRequired(), NumberRange(min=0, max=999, message='Max 3 digits')],
                      default=0)
    submit = SubmitField('Add')


