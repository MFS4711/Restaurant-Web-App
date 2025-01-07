from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from booking.models import Table, Booking

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
    # List of time slots for the day (15-minute intervals from 16:00 to 22:00)
    time_slots = [
        '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30', '17:45',
        '18:00', '18:15', '18:30', '18:45', '19:00', '19:15', '19:30', '19:45',
        '20:00', '20:15', '20:30', '20:45', '21:00', '21:15', '21:30', '21:45', '22:00'
    ]

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
            # Get start time for each time slot
            start_time = datetime.strptime(time_slot, '%H:%M').time()
            
            # Calculate the end time based on a 2-hour duration
            end_time = (datetime.combine(today, start_time) + timedelta(hours=2)).time()

            # Check if there is a booking for the table during this 2-hour time window
            conflicting_bookings = Booking.objects.filter(
                table=table,
                date=today,
                time__gte=start_time,
                time__lt=end_time
            ).exists()

            # If there is a booking, mark as "Occupied", otherwise "Available"
            availability['slots'].append({
                'time_slot': time_slot,
                'status': 'Occupied' if conflicting_bookings else 'Available'
            })

        # Add table availability to the list
        table_availability.append(availability)

    # Pass data to the context
    context = {
        'time_slots': time_slots,
        'tables': tables,
        'table_availability': table_availability,
        'today': today,
    }

    return render(request, 'dashboard/staff_dashboard.html', context)
