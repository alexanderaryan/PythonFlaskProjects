from puppyadoption import FlaskForm
from puppyadoption import FormField,StringField, SubmitField,IntegerField
#from wtforms.validators import DataRequired

class Add_form(FlaskForm):
    name = StringField("Enter the name of the puppy : ")
    submit = SubmitField("Add puppy")

class Del_form(FlaskForm):
    id = IntegerField("Enter the id of the puppy to remove : ")
    submit = SubmitField("Remove puppy")

