from flask import Flask
from webui.flaskconfig import Config

app = Flask(__name__)
app.config.from_object(Config)

from webui.webapp import routes
