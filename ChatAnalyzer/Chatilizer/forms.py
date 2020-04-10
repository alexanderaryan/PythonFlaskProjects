from flask_wtf.form import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import SubmitField


class UpdateUserForm(FlaskForm):

    chat_file = FileField('Update your exported Chat history file. Only .txt please...',
                          validators=[FileAllowed(['txt'],message="Only .txt Files are allowed")])
    submit = SubmitField('Analyze')