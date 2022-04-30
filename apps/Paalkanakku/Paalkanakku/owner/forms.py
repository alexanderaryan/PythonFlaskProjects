from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, \
    SelectField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms import ValidationError, validators
from flask_wtf.file import FileField, FileAllowed


from flask_login import current_user
try:
    from Paalkanakku.models import CowOwner
except:
    from Paalkanakku.Paalkanakku.models import CowOwner


class AddCustForm(FlaskForm):

    place = StringField('Place', validators=[DataRequired(),Length(max=30,message="Min 5 / Max 30 characters")])
    name = StringField('Name', validators=[DataRequired(),Length(max=30,message="Min 5 / Max 30 characters")])
    cows = IntegerField('Number of Cows',validators=[DataRequired(),NumberRange(min=0, max=20,message='Max No.of Cows is 20')])
    milker_id = SelectMultipleField('Milker',validators=[DataRequired()])
    submit = SubmitField('Add')


class DeleteCustForm(FlaskForm):

    checkbox = BooleanField("Delete")
    #checkbox = SelectField(u'Delete',choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Update')


class EditUserForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(),Length(max=30,message="Min 5 / Max 30 characters")])
    surname = StringField('Initial', validators=[Length(max=30, message="Min 5 / Max 30 characters")])
    place = StringField('Place', validators=[DataRequired(), Length(max=30, message="Min 5 / Max 30 characters")])
    cows = IntegerField('Number of Cows',
                        validators=[DataRequired(), NumberRange(min=0, max=20, message='Max No.of Cows is 20')])
#    milker_id = SelectMultipleField('Milker', validators=[DataRequired()])
    phone_number = IntegerField("Mobile",
                                validators=[NumberRange(min=0, max=9999999999, message='Mobile NUmber should be 10 digits'),
                                            validators.Optional()])
    address_line2 = StringField("Address Line1", validators=[])
    pincode = IntegerField("Pin", validators=[validators.Optional()])
    email = StringField("email", validators=[Email(),
                                             Length(max=60, message="Length exceeded 60"),
                                             validators.Optional()],
                        filters = [lambda x: x or None])

    # date = DateField('Date', validators=[DataRequired()])

    dairy_loan = IntegerField("DairyLoan",validators=[validators.Optional()])
    kcc_loan = IntegerField("KCCLoan",validators=[validators.Optional()])

    country = StringField("Country", validators=[])
    state = StringField("State", validators=[])
    # products = IntegerField("Punnakku", validators=[])
    # milking_charge = IntegerField("MilkingCharge", validators=[])
    # dr_service = IntegerField("Doctor Service", validators=[])
    # advance = IntegerField("Advance", validators=[])
    # loan = IntegerField("Debt", validators=[])

    submit = SubmitField('Save Profile')