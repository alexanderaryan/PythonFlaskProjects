from puppyblog import FlaskForm,StringField,SubmitField,TextAreaField,DataRequired

class BlogPostForm(FlaskForm):


    title = StringField("Title",validators=[DataRequired()])
    text = TextAreaField("Your Post goes here",validators=[DataRequired()])
    submit = SubmitField("Post")