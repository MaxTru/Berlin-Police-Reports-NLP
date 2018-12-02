"""Flask startup"""
from webui.flaskconfig import Config
from flask import Flask

import os
import shutil
import logging

# Initiate logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


app = Flask(__name__)
app.config.from_object(Config)
from webui.webapp import routes
logger.info("Flask initiated")

# After startup initialize the database.
from webui.database import db_setup
db_setup.init_db()
logger.info("Database initialized")

# After startup create fresh index of the docs for Search
if os.path.isdir(Config.INDEX):
    shutil.rmtree(Config.INDEX)
    logger.info("Existing index found and deleted (new index will be created by searcher)")

# Kill DB session once the app closes
from webui.database.db_setup import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    logger.info("Database session removed")