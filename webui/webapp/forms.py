"""Implements the forms of the Flask WebApp."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
from webui.flaskconfig import Config

class SearchForm(FlaskForm):
    """Form a user may fill to enter a search query."""
    query = StringField('What do you want to find?', validators=[DataRequired()])
    submit = SubmitField('Check Reports')

class FilterForm(FlaskForm):
    """Form a user may use to filter results."""
    order = RadioField('Ordering Form', choices=[('asc', 'Ascending'), ('desc', 'Descending'), ('none', 'Unordered')], default='desc')
    classes = RadioField('Classes Form',
                         choices=[('__label__1', Config.LABEL_CAPTIONS['__label__1']),
                                  ('__label__3', Config.LABEL_CAPTIONS['__label__3']),
                                  ('__label__4', Config.LABEL_CAPTIONS['__label__4']),
                                  ('none', Config.LABEL_CAPTIONS['none'])], default='none')
