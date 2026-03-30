from flask import Flask
from routes.main_routes import main_routes

def create_app():
    app = Flask(__name__)

    # Register routes
    app.register_blueprint(main_routes)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
