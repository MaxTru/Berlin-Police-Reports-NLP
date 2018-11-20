"""Base config for the Flask Webapp."""
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    REPORTS_PAYLOAD = os.path.abspath("./data/data.dat")
    REPORTS_METADATA = os.path.abspath("./data/reports_cleaned_metadata_2018-10-21.dat")
    REPORTS_LABELS = os.path.abspath("./starspace/results_testrun_20181110/predictions.txt")
    CONFIG_TOML = os.path.abspath("./search/config.toml")
    INDEX = os.path.abspath("idx")
    LABEL_CAPTIONS = {
        "__label__1": "Criminal Damage or Fire",
        "__label__3": "Violent Crime",
        "__label__4": "Traffic Offense",
        "none": "No Filter"
    }