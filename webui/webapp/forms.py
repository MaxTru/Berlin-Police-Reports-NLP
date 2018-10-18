"""Implements the forms of the Flask WebApp."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """Form a user may fill to enter a search query."""
    query = StringField('Query', validators=[DataRequired()])
    submit = SubmitField('Search')
