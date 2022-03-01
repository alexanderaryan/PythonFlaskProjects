from puppyadoption import DataRequired,email, EqualTo, \
    StringField, SubmitField, PasswordField, FlaskForm, ValidationError
from puppyadoption.users.models import User


class Login(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(),email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm',message="Oops! Passwords must match")])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register')


    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already')


    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username is taken!')






