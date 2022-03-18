import flask
from .__init__ import api

developers = flask.Blueprint('developers', __name__, url_prefix='/api/developers', static_folder='static')
api.register_blueprint(developers)