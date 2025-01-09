from datetime import datetime, timedelta
import calendar
from django.utils import timezone
from .models import Booking, Table

# Define opening and closing hours for each day of the week
# Days of the week are indexed: 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
OPENING_HOURS = {
    0: {"open": "16:00", "close": "22:00"},  # Monday
    1: {"open": "16:00", "close": "22:00"},  # Tuesday
    2: {"open": "16:00", "close": "22:00"},  # Wednesday
    3: {"open": "16:00", "close": "22:00"},  # Thursday
    4: {"open": "16:00", "close": "22:00"},  # Friday
    5: {"open": "16:00", "close": "22:00"},  # Saturday
    6: {"open": "16:00", "close": "22:00"},  # Sunday
}


def get_opening_hours_for_today():
    """
    Get the opening and closing time for today based on the day of the week.
    :return: Tuple (open_time, close_time) in "%H:%M" format.
    """
    today = datetime.now()
    weekday = today.weekday()  # Get the day of the week (0: Monday, 6: Sunday)

    # Retrieve the opening and closing times for today
    opening_info = OPENING_HOURS.get(
        weekday, {"open": "16:00", "close": "00:00"})

    return opening_info["open"], opening_info["close"]


def generate_time_slots(open_time=None, close_time=None, interval_minutes=15):
    """
    Generate a list of time slots based on the start and end time with the given interval.

    :param open_time: The opening time in "%H:%M" format.
    :param close_time: The closing time in "%H:%M" format.
    :param interval_minutes: The interval between time slots in minutes.
    :return: List of time slots in "%H:%M" format.
    """
    # If open_time and close_time are not provided, get them dynamically
    if not open_time or not close_time:
        open_time, close_time = get_opening_hours_for_today()

    # Handle the special case where close_time is '00:00' (midnight), treat it as '23:59'
    if close_time == "00:00":
        close_time = "23:59"

    # Convert opening and closing times to datetime objects
    start_time = datetime.strptime(open_time, "%H:%M")
    end_time = datetime.strptime(close_time, "%H:%M")

    time_slots = []
    while start_time <= end_time:
        time_slots.append(start_time.strftime("%H:%M"))
        # Increment by the defined interval
        start_time += timedelta(minutes=interval_minutes)

    return time_slots


def is_table_available(table, booking_date, start_time, end_time):
    """
    Checks if the table is available for the given time range on the given date.
    :param table: The table to check.
    :param booking_date: The date of the booking.
    :param start_time: The start time of the booking.
    :param end_time: The end time of the booking.
    :return: True if the table is available, False if there is a conflict.
    """
    # Fetch all bookings for the selected table on the selected date
    conflicting_bookings = Booking.objects.filter(
        table=table,
        date=booking_date
    ).exclude(id=None)

    # Check for time conflicts
    for booking in conflicting_bookings:
        existing_start_time = timezone.make_aware(
            datetime.combine(booking.date, booking.time))
        existing_end_time = existing_start_time + timedelta(hours=2)

        # If the new booking overlaps within the 2-hour window, return False
        if (start_time < existing_end_time and end_time > existing_start_time):
            return False
    return True


def generate_conflicting_time_range(booking_date, booking_time):
    """
    Given a booking date and time, generates the start and end time of the proposed booking,
    along with a 2-hour buffer for conflict checking.
    :param booking_date: The date of the booking.
    :param booking_time: The start time of the booking.
    :return: A tuple of (start_time, end_time, conflicting_time_range_start, conflicting_time_range_end).
    """
    new_start_time = timezone.make_aware(
        datetime.combine(booking_date, booking_time))
    new_end_time = new_start_time + timedelta(hours=2)

    conflicting_time_range_start = new_start_time - timedelta(hours=2)
    conflicting_time_range_end = new_end_time

    return new_start_time, new_end_time, conflicting_time_range_start, conflicting_time_range_end


def get_table_availability_for_day(booking_date, time_slots):
    """
    Get the availability of all tables for a given day and time slots.
    :param booking_date: The date for which availability is being checked.
    :param time_slots: A list of time slots to check availability for.
    :return: List of dictionaries with table availability for each time slot.
    """
    tables = Table.objects.all()
    table_availability = []

    for table in tables:
        availability = {'table_number': table.table_number, 'slots': []}

        for time_slot in time_slots:
            start_time = datetime.strptime(time_slot, '%H:%M').time()

            new_start_time, new_end_time, _, _ = generate_conflicting_time_range(
                booking_date, start_time)
            is_available = is_table_available(
                table, booking_date, new_start_time, new_end_time)

            availability['slots'].append({
                'time_slot': time_slot,
                'status': 'Occupied' if not is_available else 'Available'
            })

        table_availability.append(availability)

    return table_availability
