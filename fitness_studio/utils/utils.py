import pytz
from flask import abort
from datetime import datetime


def validate_timezone(tz):
    """
    Validates whether the given timezone string is a recognized timezone.

    Args:
        tz (str): Timezone string to validate (e.g., "Asia/Kolkata").

    Raises:
        400 Bad Request: If the provided timezone is invalid.
    """
    try:
        pytz.timezone(tz)
    except pytz.UnknownTimeZoneError:
        abort(400, message=f"Invalid timezone '{tz}' provided!")


def convert_timezone(original_tz_str, target_tz_str):
    """
    Converts original timezone to the target timezone.

    Args:
        original_tz_str (str): Original timezone string.
        target_tz_str (str): Target timezone string
        (e.g., "UTC", "America/New_York").

    Returns:
        str: Datetime string converted to the target timezone,
        formatted as 'YYYY-MM-DD HH:MM:SS'.
    """
    target_tz = pytz.timezone(target_tz_str)
    original_dt = datetime.fromisoformat(original_tz_str)
    return original_dt.astimezone(target_tz).strftime("%Y-%m-%d %H:%M:%S")
