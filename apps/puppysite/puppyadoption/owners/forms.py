from puppyadoption import FlaskForm
from puppyadoption import FormField,StringField, SubmitField,IntegerField
#from wtforms.validators import DataRequired

class Add_form(FlaskForm):
    name = StringField("Enter the name of the owner")
    id =  StringField("Enter the id of the puppy")
    submit = SubmitField("Add owner")