"""Flask startup"""
from flask import Flask
from webui.flaskconfig import Config
import shutil
import os

app = Flask(__name__)
app.config.from_object(Config)

from webui.webapp import routes

# After startup initialize the database.
from webui.database import db_setup
db_setup.init_db()

# After startup create fresh index of the docs for Search
#import metapy
#if os.path.isdir(Config.INDEX):
#    shutil.rmtree(Config.INDEX)
#idx = metapy.index.make_inverted_index(Config.CONFIG_TOML)

# Kill DB session once the app closes
from webui.database.db_setup import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()