import flask

error_500 = flask.Blueprint('500', __name__, static_folder='../../static')