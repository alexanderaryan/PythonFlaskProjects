from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, \
    SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed


from flask_login import current_user
try:
    from Paalkanakku.models import CowOwner
except:
    from Paalkanakku.Paalkanakku.models import CowOwner


class AddCustForm(FlaskForm):

    place = StringField('Place', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    cows = IntegerField('Number of Cows',validators=[DataRequired()])
    milker_id = SelectMultipleField('Milker',validators=[DataRequired()])
    submit = SubmitField('Add')


class DeleteCustForm(FlaskForm):

    checkbox = BooleanField("Delete")
    #checkbox = SelectField(u'Delete',choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Update')

"""
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords Must Match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Register!")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered Already!")

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Entered username is taken by someone!")


class UpdateUserForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])

    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(
                            ['jpg', 'jpeg', 'png'],
                            "The format can be uploaded is .jpg,.jpeg,.png"
                            )]
                        )
    pic = FileField()
    submit = SubmitField("Update!")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered Already!")

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Entered username is taken by someone!")
"""