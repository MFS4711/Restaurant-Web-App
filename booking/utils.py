from datetime import datetime, timedelta
import calendar

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
    opening_info = OPENING_HOURS.get(weekday, {"open": "16:00", "close": "00:00"})
    
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
        start_time += timedelta(minutes=interval_minutes)  # Increment by the defined interval
    
    return time_slots