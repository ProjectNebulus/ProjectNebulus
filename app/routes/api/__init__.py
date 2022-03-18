import flask

api = flask.Blueprint('api', __name__, url_prefix='/api', static_folder='static', template_folder='templates')