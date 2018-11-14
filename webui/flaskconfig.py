"""Base config for the Flask Webapp."""
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    REPORTS_PAYLOAD = os.path.abspath("./data/data.dat")
    REPORTS_METADATA = os.path.abspath("./data/reports_cleaned_metadata_2018-10-21.dat")
