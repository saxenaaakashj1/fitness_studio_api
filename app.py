from flask import Flask
from flask_smorest import Api
from resources.bookings import blueprint as bookings_blueprint
from resources.classes import blueprint as classes_blueprint

# Initialize the Flask application
app = Flask(__name__)

# App configuration for API behavior and documentation
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Fitness Studio REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"

# Configuration for Swagger UI (API docs)
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_URL"] = (
    "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.18.1/"
)

# Initialize the Flask-Smorest API wrapper
api = Api(app)

# Register API blueprints for routes related to bookings and classes
api.register_blueprint(bookings_blueprint)
api.register_blueprint(classes_blueprint)
