from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from booking.models import Table, Booking
from booking.utils import generate_time_slots, is_table_available, generate_conflicting_time_range

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

    # Fetch all tables (to be displayed in rows)
    tables = Table.objects.all()

    # Initialize an empty list to store table availability for each time slot
    table_availability = []

    # Loop through each table and check the availability for each time slot
    for table in tables:
        availability = {'table_number': table.table_number, 'slots': []}

        # Loop through each time slot to check if the table is occupied
        for time_slot in time_slots:
            start_time = datetime.strptime(time_slot, '%H:%M').time()

            # Generate end time and conflicting time range using the utility function
            new_start_time, new_end_time, _, _ = generate_conflicting_time_range(today, start_time)

            # Check if the table is available for this time slot using the utility function
            is_available = is_table_available(table, today, new_start_time, new_end_time)

            # Append availability status
            availability['slots'].append({
                'time_slot': time_slot,
                'status': 'Occupied' if not is_available else 'Available'
            })

        # Add the table's availability to the list
        table_availability.append(availability)

    # Fetch bookings for today (Confirmed and Pending)
    today_bookings = Booking.objects.filter(
        date=today, status__in=[Booking.CONFIRMED]
    ).order_by('time')

    # Pass data to the context
    context = {
        'time_slots': time_slots,
        'tables': tables,
        'table_availability': table_availability,
        'today': today,
        'today_bookings': today_bookings,
    }

    return render(request, 'dashboard/staff_dashboard.html', context)
