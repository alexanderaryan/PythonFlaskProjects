import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
    BooleanField, SelectMultipleField, FloatField, SelectField, DateField, FieldList, FormField,\
    MonthField, RadioField
from wtforms import DecimalRangeField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms import ValidationError

from flask_login import current_user

try:
    from Paalkanakku.models import Milkers
except:
    from Paalkanakku.Paalkanakku.models import Milkers


class DailyData(FlaskForm):

    class Meta:
        csrf = False

    milker_data = Milkers.query.all()
    milker_ids = [milker.milker_id for milker in milker_data]
    milkers = [(milker.milker_id, milker.name) for milker in milker_data]

    owner_id=IntegerField('CustomerId', validators=[DataRequired()])
    cust_name = StringField('Name', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    milker = SelectField('Milker', validators=[DataRequired()],choices=milkers)
    #milked_time = RadioField('AM/PM',choices=[('am','AM'),('pm','PM')])
    litre = IntegerField('Litre',
                         validators=[NumberRange(min=0, max=99, message='Max 3 digits')],
                         default=0
                          )
    ml = IntegerField('MilliLitre',
                      validators=[NumberRange(min=0, max=999, message='Max 3 digits')],
                      default=0
                      )


class AddDailyData(FlaskForm):

    milked_date = DateField('Date', validators=[DataRequired()])
    milked_time = RadioField('Time', choices=[('am', 'AM'), ('pm', 'PM')],default="am")
    daily_data = FieldList(FormField(DailyData),
                           min_entries=1,
                           max_entries=100)
    
    submit = SubmitField('Add')


class LedgerView(FlaskForm):

    month = MonthField('Month', validators=[DataRequired()])
    submit = SubmitField('Ok', validators=[DataRequired()])

