from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.recaptcha import RecaptchaField

from flask_login import current_user
try:
    from Paalkanakku.models import User
except:
    from Paalkanakku.Paalkanakku.models import User

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email(), Length(min=1,max=50,message="Please Enter valid email")])
    username = StringField('Username',validators=[DataRequired(), Length(min=5,max=15,message="Min 6 and max 15 characters allowed")])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=25,message="Min Length is 6"),EqualTo('pass_confirm', message='Passwords Must Match')])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
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
