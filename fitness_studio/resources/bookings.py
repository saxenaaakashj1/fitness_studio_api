from fitness_studio.schemas.schemas import (
    CreateBookingRequestSchema,
    BookingResponseSchema,
    BookingQuerySchema,
)
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from datetime import datetime, timezone
from fitness_studio.utils.utils import convert_timezone, validate_timezone
from fitness_studio.models.db import connection
from email_validator import validate_email, EmailNotValidError

# Blueprint for booking-related routes
blueprint = Blueprint(
    "Bookings",
    __name__,
    description="Endpoints to create a booking & view client-specific bookings",
)


@blueprint.route("/bookings")
class GetBookings(MethodView):
    """
    GET endpoint to retrieve bookings for a specific client email.

    Query Parameters:
        email (str): Client email (required)
        timezone (str): Timezone name (default: Asia/Kolkata)

    Returns:
        List of bookings associated with the provided email, with datetime
        converted to the requested timezone.
    """

    @blueprint.arguments(BookingQuerySchema, location="query")
    @blueprint.response(200, BookingResponseSchema(many=True))
    def get(self, args):
        """Retrieve all client-specific bookings."""
        client_email = args.get("email")
        if not client_email:
            abort(400, message="Missing required query parameter: 'email'.")
        client_email = client_email.lower()
        tz = args.get("timezone", "Asia/Kolkata")
        validate_timezone(tz)
        try:
            validate_email(client_email)
        except EmailNotValidError as e:
            abort(400, message=str(e))
        with connection:
            cursor = connection.cursor()
            # Fetch bookings along with class details
            records = cursor.execute(
                """
                SELECT bookings.id, bookings.client_name, bookings.client_email, 
                bookings.booked_at, classes.id, classes.name, classes.datetime, 
                classes.instructor 
                FROM bookings JOIN classes 
                ON bookings.class_id = classes.id 
                WHERE client_email = ?""",
                (client_email,),
            ).fetchall()
            if not records:
                abort(
                    404,
                    message=f"No bookings found for email: {client_email}.",
                )
            # Format each booking and convert timezones for API response
            bookings = [
                {
                    "id": record[0],
                    "client_name": record[1],
                    "client_email": record[2],
                    "booked_at": convert_timezone(record[3], tz),
                    "class_id": record[4],
                    "name": record[5],
                    "datetime": convert_timezone(record[6], tz),
                    "instructor": record[7],
                }
                for record in records
            ]

        return bookings


@blueprint.route("/book")
class CreateBookings(MethodView):
    """
    POST endpoint to create a new booking for a class.

    Request Body:
        Follows CreateBookingRequestSchema with class_id, client_name,
        client_email.

    Query Parameters:
        timezone (str): Timezone name (default: Asia/Kolkata)

    Returns:
        Details of the created booking with timestamps in the
        requested timezone.
    """

    @blueprint.arguments(CreateBookingRequestSchema)
    @blueprint.response(201, BookingResponseSchema)
    def post(self, booking):
        """Create a new booking for a class."""
        with connection:
            cursor = connection.cursor()
            # Check if class exists and fetch its details
            classes = cursor.execute(
                """
                SELECT id, name, datetime, instructor, available_slots 
                FROM classes WHERE id = ?""",
                (booking["class_id"],),
            ).fetchone()
            if not classes:
                abort(
                    404,
                    message=f"Class with ID '{booking['class_id']}' does not exist.",
                )
            class_id, name, class_datetime, instructor, available_slots = (
                classes
            )
            if available_slots <= 0:
                abort(
                    400,
                    message=f"Class ID '{class_id}' has no available slots.",
                )
            client_email = booking["client_email"].lower()
            # Check if booking already exists for the same class and email
            already_exist = cursor.execute(
                """
                SELECT 1 FROM bookings WHERE class_id = ? AND client_email = ?
                """,
                (class_id, client_email),
            ).fetchone()
            if already_exist:
                abort(409, message="You have already booked this class.")
            # Reserve a slot in the class
            cursor.execute(
                """
                UPDATE classes SET available_slots = available_slots - 1 
                WHERE id = ?
                """,
                (class_id,),
            )
            booked_at = datetime.now(timezone.utc).isoformat()
            # Insert booking record
            cursor.execute(
                """
            INSERT INTO bookings (class_id, client_name, client_email, booked_at)
            VALUES (?, ?, ?, ?)
            """,
                (
                    booking["class_id"],
                    booking["client_name"],
                    client_email,
                    booked_at,
                ),
            )
            booking_id = cursor.lastrowid

        # Return booking details including metadata
        return {
            **booking,
            "id": booking_id,
            "name": name,
            "instructor": instructor,
        }
