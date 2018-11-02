from flask import Flask
from webui.flaskconfig import Config

cfg = 'config.toml'

app = Flask(__name__)
app.config.from_object(Config)

from webui.webapp import routes
