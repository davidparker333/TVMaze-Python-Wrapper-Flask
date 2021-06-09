from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TVShowSearchForm(FlaskForm):
    title = StringField('TV Show Title', validators=[DataRequired()])
    submit = SubmitField()