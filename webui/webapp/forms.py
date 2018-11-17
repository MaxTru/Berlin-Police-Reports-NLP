"""Implements the forms of the Flask WebApp."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    """Form a user may fill to enter a search query."""
    query = StringField('What do you want to find?', validators=[DataRequired()])
    submit = SubmitField('Check Reports')

class OrderingForm(FlaskForm):
    """Form a user may use to define how the results shall be ordered."""
    order = RadioField('Ordering Form', choices=[('asc', 'Ascending'), ('desc', 'Descending'), ('none', 'Unordered')], default='desc')

class ClassesForm(FlaskForm):
    """Form a user may use to filter on different types of crimes."""
    classes = RadioField('Classes Form', choices=[('__label__1', 'Criminal Damage or Fire'), ('__label__3', 'Violent Crime'), ('__label__4', 'Traffic Offense'), ('none', 'No Filter')], default='none')