from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg, Sum
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.utils.timezone import localdate
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from booking.models import Table, Booking
from booking.forms import BookingFilterForm
from booking.utils import generate_time_slots, is_table_available, generate_conflicting_time_range, get_table_availability_for_day

# Create your views here.

@login_required
def customer_dashboard(request, user_id):
    """

    """
    # Check if the logged-in user is the same as the user_id in the URL
    if request.user.id != int(user_id):
        # If they are not the same, redirect to a different page, for example, a 404 or the homepage
        raise Http404("You are not authorized to view this page.")
    
    user = get_object_or_404(User, id=user_id)

    # Get current date and time for comparisons
    current_time = timezone.now()

    # Fetch upcoming bookings (bookings that are in the future)
    upcoming_bookings = Booking.objects.filter(user=user, date__gte=current_time.date(
    ), time__gte=current_time.time(), status__in=['confirmed', 'pending']).order_by('date', 'time')

    # Fetch past bookings (bookings that are in the past)
    past_bookings = Booking.objects.filter(user=user, date__lt=current_time.date(
    ), status='completed').order_by('-date', '-time')

    # Fetch customer action required bookings (status 'customer_confirmation_required')
    customer_action_required_bookings = Booking.objects.filter(
        user=user, status=Booking.CUSTOMER_CONFIRMATION_REQUIRED).order_by('date', 'time')

    context = {
        'user': user,
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'customer_action_required_bookings': customer_action_required_bookings,
    }

    return render(request, 'dashboard/customer_dashboard.html', context)

# Custom decorator to check if the user is a staff member
def is_staff(user):
    return user.is_staff

@login_required(login_url='/login/')  # redirect to login page if not authenticated
@user_passes_test(is_staff, login_url='/unauthorized/')
def staff_dashboard(request):
    """

    """
    # Use the utility function to generate time slots with dynamic opening hours
    time_slots = generate_time_slots(interval_minutes=15)

    # Get today's date
    today = timezone.now().date()

    # Get table availability using the utility function
    table_availability = get_table_availability_for_day(today, time_slots)

    # Fetch bookings for today (Confirmed and Pending)
    today_bookings = Booking.objects.filter(
        date=today, status__in=[Booking.CONFIRMED]
    ).order_by('time')

    # Pass data to the context
    context = {
        'time_slots': time_slots,
        'table_availability': table_availability,
        'today': today,
        'today_bookings': today_bookings,
    }

    return render(request, 'dashboard/staff_dashboard.html', context)


# Custom decorator to check if the user is a staff member
def is_superuser(user):
    return user.is_superuser


@login_required(login_url='/login/')  # redirect to login page if not authenticated
@user_passes_test(is_superuser, login_url='/unauthorized/')
def admin_dashboard(request):
    """

    """
    # Get today's date
    today = timezone.now().date()

    # Initialize the filter form
    filter_form = BookingFilterForm(request.GET)

    # Set default dates (today) for the view if no form submission
    start_date = end_date = today

    # Apply filter logic
    if filter_form.is_valid():
        # Get the date range based on selected filter
        start_date, end_date = filter_form.get_filtered_date_range()

    # Fetch bookings based on the filtered date range
    bookings = Booking.objects.filter(date__range=[start_date, end_date])

    # Calculate booking statistics
    total_bookings = bookings.count()
    total_confirmed = bookings.filter(status=Booking.CONFIRMED).count()
    total_pending = bookings.filter(status=Booking.PENDING).count()
    total_cancelled = bookings.filter(status=Booking.CANCELLED).count()
    total_no_show = bookings.filter(status=Booking.NO_SHOW).count()

    # Calculate overall statistics
    if total_bookings > 0:
        # Average Booking Size (total number of people / total bookings)
        avg_booking_size = bookings.aggregate(Avg('number_of_people'))['number_of_people__avg']
        
        # Average Bookings Per Day (total bookings / number of days in range)
        num_days = (end_date - start_date).days + 1  # +1 to include both start and end days
        avg_bookings_per_day = total_bookings / num_days

        # Average Number of Visitors per Day (total number of people / number of days in range)
        total_visitors = bookings.aggregate(Sum('number_of_people'))['number_of_people__sum']
        avg_visitors_per_day = total_visitors / num_days if total_visitors else 0
    else:
        avg_booking_size = avg_bookings_per_day = avg_visitors_per_day = 0

    # Context for template rendering
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