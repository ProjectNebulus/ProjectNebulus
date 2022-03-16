"""
App entrypoint.
"""
from app import init_app, simple_page
from waitress import serve

app = init_app()
app.register_blueprint(simple_page)

if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    serve(app=app, host="localhost", port=8080)
