"""Implements the forms of the Flask WebApp."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """Form a user may fill to enter a search query."""
    query = StringField('What do you want to find?', validators=[DataRequired()])
    submit = SubmitField('Check Reports')

class FilterForm(FlaskForm):
    """Form a user may use to filter results."""
    order = RadioField('Ordering Form', choices=[('asc', 'Ascending'), ('desc', 'Descending'), ('none', 'Unordered')], default='desc')
    classes = RadioField('Classes Form',
                         choices=[('__label__1', 'Criminal Damage or Fire'), ('__label__3', 'Violent Crime'),
                                  ('__label__4', 'Traffic Offense'), ('none', 'No Filter')], default='none')
