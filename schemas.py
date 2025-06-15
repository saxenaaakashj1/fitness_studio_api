from marshmallow import fields, Schema


class CreateBookingRequestSchema(Schema):
    """
    Schema for validating incoming booking requests.

    Fields:
        class_id (int): ID of the class being booked (required).
        client_name (str): Name of the client (required).
        client_email (str): Valid email of the client (required).
    """

    class_id = fields.Int(required=True)
    client_name = fields.Str(required=True)
    client_email = fields.Email(required=True)


class BookingResponseSchema(Schema):
    """
    Schema for serializing booking data returned in responses.

    All fields are marked as dump_only since they are read-only
    outputs.
    """

    id = fields.Int(dump_only=True)
    class_id = fields.Int(dump_only=True)
    client_name = fields.Str(dump_only=True)
    client_email = fields.Email(dump_only=True)
    name = fields.Str(dump_only=True)
    datetime = fields.Str(dump_only=True)
    instructor = fields.Str(dump_only=True)
    booked_at = fields.Str(dump_only=True)


class ClassResponseSchema(Schema):
    """
    Schema for serializing class details.

    All fields are dump_only, used when sending class data to clients.
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    datetime = fields.Str(dump_only=True)
    instructor = fields.Str(dump_only=True)
    available_slots = fields.Int(dump_only=True)


class BookingQuerySchema(Schema):
    """
    Schema for validating query parameters for fetching bookings.

    Fields:
        email (str): Required email of the client to filter bookings.
        timezone (str): Optional timezone for datetime conversion.
        Defaults to 'Asia/Kolkata'.
    """

    email = fields.Email(
        required=True, metadata={"description": "Client email address"}
    )
    timezone = fields.Str(
        required=False,
        load_default="Asia/Kolkata",
        metadata={"description": "Timezone name (default: Asia/Kolkata)"},
    )


class TimezoneQuerySchema(Schema):
    """
    Schema for validating optional timezone parameter in query.

    Fields:
        timezone (str): Optional timezone for datetime formatting.
        Defaults to 'Asia/Kolkata'.
    """

    timezone = fields.Str(
        required=False,
        load_default="Asia/Kolkata",
        metadata={"description": "Timezone name (default: Asia/Kolkata)"},
    )
