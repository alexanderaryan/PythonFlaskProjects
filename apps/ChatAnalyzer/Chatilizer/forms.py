from flask_wtf.form import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import SubmitField
from flask_wtf.recaptcha import RecaptchaField,Recaptcha





class UpdateUserForm(FlaskForm):

    chat_file = FileField('Update your exported Chat history file. Only .txt please...',
                          validators=[FileRequired(message="Buddy!! Only .txt Files are allowed!!"),
                                      FileAllowed(['txt'],message="Buddy!! Only .txt Files are allowed!!")])
    recaptcha = RecaptchaField()

    submit = SubmitField('Analyze')