"""
App entrypoint.
"""
from app.routes import init_app
from waitress import serve
from app.routes.main_blueprint import main_blueprint

app = init_app()
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    serve(app=app, host="localhost", port=8080)
