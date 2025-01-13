from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Sum
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.timezone import localdate

from booking.forms import BookingFilterForm
from booking.models import Booking
from booking.utils import generate_time_slots, get_table_availability_for_day

# Create your views here.


@login_required(login_url='/accounts/login/')
def customer_dashboard(request, user_id):
    """
    Handles the customer dashboard view, displaying a list of upcoming, past,
    and customer action-required bookings for a specific user.

    **Context:**
    - user: The user whose dashboard is being viewed.
    - upcoming_bookings: Bookings for the user that are in the future.
    - past_bookings: Completed bookings for the user in the past.
    - customer_action_required_bookings: Bookings requiring customer
    confirmation.

    **Template:**
    :template:`dashboard/customer_dashboard.html`
    """
    # Ensure the logged-in user matches the user_id in the URL
    if request.user.id != int(user_id):
        # add an error message and redirect to the homepage.
        messages.error(request, "You are not authorised to access this page.")
        return redirect('/')

    # Retrieve the user object, ensuring it exists in the database
    user = get_object_or_404(User, id=user_id)

    # Get the current time to filter bookings accordingly
    current_time = timezone.now()

    # Fetch upcoming bookings (those scheduled in the future)
    upcoming_bookings = Booking.objects.filter(
        user=user,
        status__in=['confirmed', 'pending']
    ).order_by('date', 'time')

    # Fetch past bookings (those already completed)
    past_bookings = Booking.objects.filter(
        user=user, date__lt=current_time.date(), status='completed'
    ).order_by('-date', '-time')

    # Fetch bookings requiring customer confirmation
    customer_action_required_bookings = Booking.objects.filter(
        user=user, status=Booking.CUSTOMER_CONFIRMATION_REQUIRED
    ).order_by('date', 'time')

    # If there are bookings requiring customer confirmation, add a message
    if customer_action_required_bookings.exists():
        messages.info(
            request, "Your booking time has been updated. \
            Please review and take the necessary actions.")

    # Pass all relevant data to the template context for rendering
    context = {
        'user': user,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'customer_action_required_bookings': customer_action_required_bookings,
    }

    return render(request, 'dashboard/customer_dashboard.html', context)


# Redirect to login if the user is not authenticated
@login_required(login_url='/accounts/login/')
def staff_dashboard(request):
    """
    Handles the staff dashboard view, displaying table availability for today,
    and the bookings scheduled for today.

    **Context:**
    - time_slots: Generated time slots for the day.
    - table_availability: Availability of tables based on generated time slots.
    - today: Today's date.
    - today_bookings: Bookings for today that are confirmed.

    **Template:**
    :template:`dashboard/staff_dashboard.html`
    """
    if not request.user.is_staff:
        # If the user is not a staff member, add an error message and redirect
        messages.error(request, "You are not authorised to access this page.")
        return redirect('/')
    
    # Generate time slots with dynamic opening hours 15-minute intervals
    time_slots = generate_time_slots(interval_minutes=15)

    # Get today's date for scheduling and availability checks
    today = timezone.now().date()

    # Check table availability for current day using the generated time slots
    table_availability = get_table_availability_for_day(today, time_slots)

    # Fetch confirmed bookings for today
    today_bookings = Booking.objects.filter(
        date=today, status__in=[Booking.CONFIRMED]
    ).order_by('time')

    # Pass all the data to the template for rendering
    context = {
        'time_slots': time_slots,
        'table_availability': table_availability,
        'today': today,
        'today_bookings': today_bookings,
    }

    return render(request, 'dashboard/staff_dashboard.html', context)


# Redirect to login if the user is not authenticated
@login_required(login_url='/accounts/login/')
def admin_dashboard(request):
    """
    Handles the admin dashboard view, providing an overview of booking
    statistics  based on a filter range for booking dates.
    Displays the total number of bookings
    and various statistics on booking status and sizes.

    **Context:**
    - filter_form: The form used for filtering bookings by date range.
    - bookings: The bookings within the filtered date range.
    - total_bookings: The total count of bookings within the date range.
    - total_confirmed: The total number of confirmed bookings.
    - total_pending: The total number of pending bookings.
    - total_cancelled: The total number of cancelled bookings.
    - total_no_show: The total number of no-show bookings.
    - start_date: The start date of the filter range.
    - end_date: The end date of the filter range.
    - avg_booking_size: The average number of people per booking.
    - avg_bookings_per_day: The average number of bookings
    per day in the date range.
    - avg_visitors_per_day: The average number of visitors
    per day in the date range.

    **Template:**
    :template:`dashboard/admin_dashboard.html`
    """
    if not request.user.is_superuser:
        # If the user is not a superuser, add an error message and redirect
        messages.error(request, "You are not authorised to access this page.")
        return redirect('/')
    
    # Get today's date for use in filtering and statistics calculations
    today = timezone.now().date()

    # Initialize the filter form so admin can filter bookings by date range
    filter_form = BookingFilterForm(request.GET)

    # Set default dates to today in case the filter form is not submitted
    start_date = end_date = today

    # If the filter form is valid, apply the filtered date range
    if filter_form.is_valid():
        start_date, end_date = filter_form.get_filtered_date_range()

    # Fetch bookings that fall within the specified date range
    bookings = Booking.objects.filter(date__range=[start_date, end_date])

    # Calculate various statistics for bookings in the selected date range
    total_bookings = bookings.count()  # Total number of bookings
    total_confirmed = bookings.filter(
        status=Booking.CONFIRMED).count()  # Total confirmed bookings
    total_pending = bookings.filter(
        status=Booking.PENDING).count()  # Total pending bookings
    total_cancelled = bookings.filter(
        status=Booking.CANCELLED).count()  # Total cancelled bookings
    total_no_show = bookings.filter(
        status=Booking.NO_SHOW).count()  # Total no-show bookings

    # Calculate averages if there are bookings in the selected date range
    if total_bookings > 0:
        # Average booking size: total number of people / total bookings
        avg_booking_size = bookings.aggregate(Avg('number_of_people'))[
            'number_of_people__avg']

        # Average bookings per day: total bookings / number of days in range
        # +1 to include both start and end days
        num_days = (end_date - start_date).days + 1
        avg_bookings_per_day = total_bookings / num_days

        # Average visitors per day: total number of visitors / number of days
        total_visitors = bookings.aggregate(Sum('number_of_people'))[
            'number_of_people__sum']
        avg_visitors_per_day = (
            total_visitors / num_days if total_visitors else 0
        )
    else:
        # If no bookings, set averages to 0
        avg_booking_size = avg_bookings_per_day = avg_visitors_per_day = 0

    # Pass all relevant data to the context for rendering the admin template
    context = {
        'filter_form': filter_form,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'total_confirmed': total_confirmed,
        'total_pending': total_pending,
        'total_cancelled': total_cancelled,
        'total_no_show': total_no_show,
        'start_date': start_date,
        'end_date': end_date,
        'avg_booking_size': avg_booking_size,
        'avg_bookings_per_day': avg_bookings_per_day,
        'avg_visitors_per_day': avg_visitors_per_day,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)
