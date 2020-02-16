from dress_me.dressme import StringField,FlaskForm,DataRequired,SubmitField,\
    FormField, FieldList, Form, DateField
from datetime import datetime


def present_or_future_date(value):
    if value < datetime.date.today():
        raise FlaskForm.ValidationError("The date cannot be in the past!")
    return value
"""class MaleForm(FlaskForm):

    shirt = StringField("Shirt",validators=[DataRequired()])
    pants = StringField("Pants", validators=[DataRequired()])
    submit = SubmitField("I am done!")"""


class FemaleForm(FlaskForm):

    attire = StringField("Attire",validators=[DataRequired()])
    submit = SubmitField("I am done!")


class MaleForm(Form):

    shirt = StringField("Shirt",validators=[DataRequired()])
    pants = StringField("Pants",validators=[DataRequired()])


class MainMaleForm(FlaskForm):

    attires = FieldList(
        FormField(MaleForm),
        min_entries=1,
        max_entries=100
    )
    submit = SubmitField("I am done!")


class ShuffleForm(FlaskForm):

    from_date = DateField('From', format='%Y-%m-%d', validators=[present_or_future_date])
    to_date = DateField('To', format='%Y-%m-%d',validators=[present_or_future_date])
    submit =SubmitField('Remove')