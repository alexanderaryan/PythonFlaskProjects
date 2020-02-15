from dress_me.dressme import StringField,FlaskForm,DataRequired,SubmitField,\
    FormField, FieldList, Form


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

    submit =SubmitField('Remove')