from dressme import StringField,FlaskForm,DataRequired,SubmitField,\
    FormField, FieldList, Form, SelectMultipleField,ListWidget,CheckboxInput
from datetime import datetime


def present_or_future_date(value):

    if value < datetime.date.today():
        raise FlaskForm.ValidationError("The date cannot be in the past!")
    return value

class MultiSelect(SelectMultipleField):

    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ShuffleForm(FlaskForm):

    #from_date = DateField('From', format='%Y-%m-%d', validators=[present_or_future_date])
    #to_date = DateField('To', format='%Y-%m-%d',validators=[present_or_future_date])
    from_date = StringField('From',validators=[DataRequired(message="Please select from date")])
    to_date = StringField('To',validators=[DataRequired(message="Please select to date")] )
    weekends = MultiSelect("Week Offs/Leave Days",\
                                   choices=[('0', 'Monday'), ('1','Tuesday'), ('2','Wednesday'),\
                                                             ('3','Thursday'),('4','Friday'),('5','Saturday'),\
                                                             ('6','Sunday')])
    submit = SubmitField('Schedule')


class MaleForm(Form):

    shirt = StringField("Shirt Color",render_kw={"placeholder": "White"})
    shirt_pattern = StringField("Shirt Pattern",render_kw={"placeholder": "Checked"})
    shirt_brand = StringField("Shirt Brand",render_kw={"placeholder": "Pepe"})
    pants = StringField("Pants Color",render_kw={"placeholder": "Cream"})
    pants_pattern = StringField("Pants Pattern",render_kw={"placeholder": "Plain"})
    pants_brand = StringField("Pants Brand",render_kw={"placeholder": "Indian Terrain"})



class MainMaleForm(FlaskForm):

    attires = FieldList(
        FormField(MaleForm),
        min_entries=1,
        max_entries=100,validators=[DataRequired()]
    )

    submit = SubmitField("I am done!")

class FemaleForm(Form):

    attire = StringField("Attire", validators=[DataRequired()], render_kw={"placeholder": "Yellow Chudi Black Leggings"})
    #from_date = StringField("From", validators=[DataRequired()])
    #to_date = StringField("To", validators=[DataRequired()])


class MainFemaleForm(FlaskForm):

    attires = FieldList(
        FormField(FemaleForm),
        min_entries=1,
        max_entries=100
    )
    submit = SubmitField("I am done!")

