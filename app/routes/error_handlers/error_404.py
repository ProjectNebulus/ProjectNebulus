import flask

error_404 = flask.Blueprint('404', __name__, url_prefix='/404', template_folder='templates', static_folder='static')