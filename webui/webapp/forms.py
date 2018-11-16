"""Implements the forms of the Flask WebApp."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """Form a user may fill to enter a search query."""
    query = StringField('What do you want to find?', validators=[DataRequired()])
    submit = SubmitField('Check Reports')