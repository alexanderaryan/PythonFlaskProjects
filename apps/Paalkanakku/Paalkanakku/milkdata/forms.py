import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
    BooleanField, SelectMultipleField, FloatField, SelectField, DateField, FieldList, FormField,\
    MonthField, RadioField
from wtforms import DecimalRangeField,DateField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms import ValidationError

from flask_login import current_user

try:
    from Paalkanakku.models import Milkers
    from Paalkanakku.milkers.forms import milker_data
except:
    from Paalkanakku.Paalkanakku.models import Milkers
    from Paalkanakku.Paalkanakku.milkers.forms import milker_data


class DailyData(FlaskForm):

    class Meta:
        csrf = False

    milkers=milker_data()[2]

    owner_id=IntegerField('CustomerId', validators=[DataRequired()])
    cust_name = StringField('Name', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])

    #After version 2.0
    # milker = SelectField('Milker', choices=milkers)
    #milker = SelectField('Milker', validators=[DataRequired()],choices=milkers)

    litre = IntegerField('Litre',
                         validators=[NumberRange(min=0, max=99, message='Max 3 digits')],
                         default=0
                          )
    ml = IntegerField('MilliLitre',
                      validators=[NumberRange(min=0, max=999, message='Max 3 digits')],
                      default=0
                      )
    fodder = IntegerField("Fodder", default=0,
                          validators=[validators.Optional()],
                          filters = [lambda x: x or 0])
    loan = IntegerField("Loan", default=0,
                        validators=[validators.Optional()],
                        filters=[lambda x: x or 0])
    advance = IntegerField("Advance", default=0,
                           validators=[validators.Optional()],
                           filters=[lambda x: x or 0])
    dr_service = IntegerField("Dr_Service", default=0,
                              validators=[validators.Optional()],
                              filters=[lambda x: x or 0])


class AddDailyData(FlaskForm):

    milked_date = DateField('Date', validators=[DataRequired()])
    price = FloatField("Milk Rate",validators=[DataRequired(),
                                               NumberRange(min=1, max=999,message='Price should be greater than 0')])
    milked_time = RadioField('Time', choices=[('am', 'AM'), ('pm', 'PM')],default="am")
    daily_data = FieldList(FormField(DailyData),
                           min_entries=1,
                           max_entries=100)
    milking_charge = IntegerField("Milking Charge",validators=[DataRequired()], default="0")
    
    submit = SubmitField('Add')


class LedgerView(FlaskForm):

    month = MonthField('Month', validators=[DataRequired()])
    submit = SubmitField('Take Google Backup', validators=[DataRequired()])

