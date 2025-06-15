from db import connection
from schemas import ClassResponseSchema, TimezoneQuerySchema
from flask_smorest import Blueprint
from flask.views import MethodView
from utils import convert_timezone, validate_timezone


# Blueprint for class-related routes
blueprint = Blueprint(
    "Classes",
    __name__,
    description="Endpoint to list available classes and their details",
)


@blueprint.route("/classes")
class GetClasses(MethodView):
    """
    GET endpoint to fetch all available classes.

    Optional Query Parameter:
        timezone (str): Timezone name (default: Asia/Kolkata)

    Returns:
        List of available classes with time converted to requested timezone.
    """

    @blueprint.arguments(TimezoneQuerySchema, location="query")
    @blueprint.response(200, ClassResponseSchema(many=True))
    def get(self, args):
        """Fetch all available classes."""
        with connection:
            cursor = connection.cursor()
            # Fetch all classes with available slots
            records = cursor.execute(
                "SELECT * FROM classes WHERE available_slots > 0"
            ).fetchall()
            # Get timezone from query param (default to IST)
            tz = args.get("timezone", "Asia/Kolkata")
            validate_timezone(tz)
            # Format classes for API response
            classes = [
                {
                    "id": record[0],
                    "name": record[1],
                    "datetime": convert_timezone(record[2], tz),
                    "instructor": record[3],
                    "available_slots": record[4],
                }
                for record in records
            ]

        return classes
