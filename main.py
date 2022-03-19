"""
App entrypoint.
"""
from app.routes import init_app
from waitress import serve
from app.routes.main_blueprint import main_blueprint
from app.routes.static.static_blueprint import static_blueprint
# from app.routes.error_handlers import error_blueprint
app = init_app()
app.register_blueprint(main_blueprint)
app.register_blueprint(static_blueprint)
# app.register_blueprint(error_blueprint)
if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    serve(app=app, host="localhost", port=8080)
